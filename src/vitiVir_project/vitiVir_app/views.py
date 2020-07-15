import os, glob
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializers import MyUserSerializer, ContactSerializer, RequestAccountSerializer
from .models import MyUser
from virData_app.views import EntryListView

from virData_app.serializers import EntrySerializer
from virData_app.models import Entry

from django_filters import rest_framework as filters

from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline, NcbitblastxCommandline, NcbitblastnCommandline
from Bio.Blast import NCBIXML

class UserViewSet(viewsets.ModelViewSet):
    ''' Manage and create users at /users/manageusers/'''
    
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (AllowAny,) #(permissions.UpdateUser,) #can add multiple classes to viewset

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('email',)

    # @action(detail=True, methods=['put'], name='Change Password')
    # def password(self, request, pk=None):
    #     """Update the user's password."""
    #     ...


class LoginViewSet(viewsets.ViewSet):
    '''Checks email and password, returns authtoken at /users/login/'''

    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        '''Use the ObtainAuthToken APIView to validate and create token'''
        
        token = ObtainAuthToken().post(request)
        return token


class BlastViewSet(viewsets.ViewSet):
    ''' Blastn, tblastn, or tblastx against local vitivirseq db at /api/blast/'''

    authentication_classes = (TokenAuthentication,) #still accessible when not logged in???
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = request.data.get('sequences')
        type_of_blast = request.data.get('program')
        tmp_file_path = os.path.join('/tmp', "%s.in" % timezone.now().microsecond) #time stamp for unique in case of multiple queries at once
        tmp_out_file_path = os.path.join('/tmp', "%s.out" % timezone.now().microsecond)
        evalue = float(1e-10)
        max_nb = 100000
        
        if request.data.get('evalue'):
            evalue = float(request.data.get('evalue'))

        if request.data.get('maxNbAlignments'):
            max_nb = request.data.get('maxNbAlignments')
            
        with open(tmp_file_path, 'w') as f:
            f.write(data)

        blast_path = '/var/www/vitiVir/db/blastdb/ncbi-blast-2.10.0+/bin/' + type_of_blast #'/vagrant/db/blastdb/ncbi-blast-2.10.0+/bin/' + type_of_blast
        local_db = '/var/www/vitiVir/db/blastdb/vitiVirSeq.fasta' #'/vagrant/db/blastdb/vitiVirSeq.fasta',  
        
        if type_of_blast == 'blastn':
            blast_cline = NcbiblastnCommandline(
                cmd=blast_path, 
                query=tmp_file_path, 
                db=local_db, 
                evalue=evalue,
                max_target_seqs=max_nb,
                outfmt=5, 
                out=tmp_out_file_path)
            blast_cline
            stdout, stderr = blast_cline()
        elif type_of_blast == 'tblastn':
            blast_cline = NcbitblastnCommandline(
                cmd=blast_path, 
                query=tmp_file_path, 
                db=local_db, 
                evalue=evalue,
                max_target_seqs=max_nb,
                outfmt=5, 
                out=tmp_out_file_path)
            blast_cline
            stdout, stderr = blast_cline()
        elif type_of_blast == 'tblastx':
            blast_cline = NcbitblastxCommandline(
                cmd=blast_path, 
                query=tmp_file_path, 
                db=local_db, 
                evalue=evalue,
                max_target_seqs=max_nb,
                outfmt=5, 
                out=tmp_out_file_path)
            blast_cline
            stdout, stderr = blast_cline()
        else:
            print("program type invalid")
        
        with open(tmp_out_file_path) as f:
            out = f.read()
        
        os.remove(tmp_file_path)
        os.remove(tmp_out_file_path)
        
        return Response(out, content_type='text/xml')
        

class ContactView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send()
            return Response(status=201)
        return Response(serializer.errors, status=400)


class RequestAccountView(APIView):
    permission_classes=[]
    def post(self, request):
        serializer = RequestAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send()
            return Response(status=201)
        return Response(serializer.errors, status=400)


class GetDBStatsView(APIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes=[]
    
    def get(self, request):
        total = Entry.objects.count()
        SRA_query = Entry.objects.filter(sample__contains="SRR").values('sample').distinct()
        SRA_count = len(SRA_query)
        INV_query = Entry.objects.filter(sample__contains="Inv").values('sample').distinct()
        INV_count = len(INV_query)

        local_db = '/var/www/vitiVir/db/blastdb/vitiVirSeq.fasta' #'/vagrant/db/blastdb/vitiVirSeq.fasta' 
        number_of_lines = 0
        file = open(local_db)
        for line in file:
            line = line.strip("\n")
            number_of_lines += 1
        file.close()

        viral_seq = number_of_lines/2

        taxonomies = Entry.objects.mongo_find({'blastx.taxonomy':{'$regex':''}}) #blastx taxonomy exists

        taxo_list = []
        for entry in taxonomies: 
            taxo_list.append(entry["blastx"]["taxonomy"])

        families = {}
        for i in taxo_list:
            try:
                fam = i.split(";")[2]
                if fam != "Vitaceae": #Exclude vitaceae  
                    if fam in families.keys():
                        families[fam] +=1
                    else:
                        families[fam]=1
            except:
                pass

        #convert to percentage
        sum_f = sum(families.values())
        for i in families:
            families[i] = float(families[i]/sum_f) * 100


        #format for bar chart
        format_families = {"other":0}

        for i in families:
            if families[i]>2: #if it represents more thant 2%, may need to modify
                format_families[i]=families[i]
            else:
                format_families["other"]+=families[i]
         
        families_list = []
        temp={}
        for i in format_families:
            temp["name"]=i
            temp['y']=format_families[i]
            families_list.append(temp)
            temp={}

        print("\nSTATS\ntotal:",total,"\nSRA and inv:",SRA_count, INV_count,"\nSeqs:",viral_seq,"\n",families_list)
        
        data = {"total":total,"SRA_count":SRA_count,"INV_count":INV_count,"viral_seq_count":viral_seq,"families":families_list}
        
        return Response(data, content_type='text')