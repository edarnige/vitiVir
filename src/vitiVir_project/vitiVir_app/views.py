#Views dealing with users, contact, BLAST, and statistics

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
    ''' 
    Manage and create users at /users/manageusers/
    '''
    
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (AllowAny,) #(permissions.UpdateUser,) #can add multiple classes to viewset

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('email',)

    # Maybe add password changing in the future
    # @action(detail=True, methods=['put'], name='Change Password')
    # def password(self, request, pk=None):
    #     """Update the user's password."""
    #     ...


class LoginViewSet(viewsets.ViewSet):
    '''
    Checks email and password, returns authtoken at /users/login/
    '''

    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        '''
        Use the ObtainAuthToken APIView to validate and create token
        '''
        
        token = ObtainAuthToken().post(request)
        return token


class BlastViewSet(viewsets.ViewSet):
    '''
    Blastn, tblastn, or tblastx against local vitivirseq db at /api/blast/
    '''

    authentication_classes = (TokenAuthentication,) #still accessible when not logged in???
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        '''
        Execute BLAST command and return XML results to front end
        '''

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

        blast_path = '/var/www/vitiVir/db/blastdb/ncbi-blast-2.10.0+/bin/' + type_of_blast 
        local_db = '/var/www/vitiVir/db/blastdb/vitiVirSeq.fasta' 

        #Development mode:
        # blast_path = '/vagrant/db/blastdb/ncbi-blast-2.10.0+/bin/' + type_of_blast
        # local_db = '/vagrant/db/blastdb/vitiVirSeq.fasta'

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
    '''
    Contact form 
    '''

    permission_classes = []

    def post(self, request):
        '''
        Contact form request and response
        '''

        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send()
            return Response(status=201)
        return Response(serializer.errors, status=400)


class RequestAccountView(APIView):
    '''
    Request and account
    '''

    permission_classes=[]

    def post(self, request):
        '''
        Request account request and response
        '''

        serializer = RequestAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send()
            return Response(status=201)
        return Response(serializer.errors, status=400)


class GetDBStatsView(APIView):
    '''
    Generate VitiVir DB statistics and send to front-end
    '''

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes=[]
    
    def get(self, request):
        '''
        Get all required data: total entries, samples included, numebr of viral sequences
        and data for pie/donut charts
        '''

        total = Entry.objects.count()
        SRA_query = Entry.objects.filter(sample__contains="SRR").values('sample').distinct()
        SRA_count = len(SRA_query)
        INV_query = Entry.objects.filter(sample__contains="Inv").values('sample').distinct()
        INV_count = len(INV_query)

        local_db = '/var/www/vitiVir/db/blastdb/vitiVirSeq.fasta'
        # Development mode:
        # local_db = '/vagrant/db/blastdb/vitiVirSeq.fasta' 

        number_of_lines = 0
        file = open(local_db)
        for line in file:
            line = line.strip("\n")
            number_of_lines += 1
        file.close()

        viral_seq = number_of_lines/2

        #Get all taxonomic notations from VitiVir entries
        taxonomies = Entry.objects.mongo_find({'blastx.taxonomy':{'$regex':''}}) #blastx taxonomy exists

        taxo_list = []
        for entry in taxonomies: 
            taxo_list.append(entry["blastx"]["taxonomy"])

        #Global family overview dictionary
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


        #Viruses only dictionaries by genome type
        ss_viruses = {}
        ds_viruses = {}
        other_viruses = {}
        for i in taxo_list:
            try:
                dom = i.split(";")[0]
                if dom == "Viruses":
                    vir_fam = i.split(";")[2]
                    vir_genome = i.split(";")[1]
                    
                    if vir_genome == "ssRNA viruses":
                        if vir_fam in ss_viruses.keys():
                            ss_viruses[vir_fam] += 1
                        elif vir_fam !='': #if not blank
                            ss_viruses[vir_fam] = 1

                    elif vir_genome == "dsRNA viruses":
                        if vir_fam in ds_viruses.keys():
                            ds_viruses[vir_fam] += 1
                        elif vir_fam !='': #if not blank
                            ds_viruses[vir_fam] = 1

                    else: #ssDNA
                        if vir_fam in other_viruses.keys():
                            other_viruses[vir_fam] += 1
                        elif vir_fam != '':
                            other_viruses[vir_fam] = 1
            except:
                pass



        #Convert to percentage
        sum_f = sum(families.values())
        for i in families:
            families[i] = float(families[i]/sum_f) * 100
        sum_ss = sum(ss_viruses.values())
        for i in ss_viruses:
            ss_viruses[i] = float(ss_viruses[i]/sum_ss) * 100 
        sum_ds = sum(ds_viruses.values())
        for i in ds_viruses:
            ds_viruses[i] = float(ds_viruses[i]/sum_ds) * 100
        sum_other = sum(other_viruses.values())
        for i in other_viruses:
            other_viruses[i] = float(other_viruses[i]/sum_other) * 100

        sum_all_viruses = sum_ss+ sum_ds + sum_other

        #Format data for pie chart
        format_families = {"other (<1%)":0}

        for i in families:
            if families[i]>1: #if it represents more thant 1%, may need to modify
                format_families[i]=families[i]
            else:
                format_families["other (<1%)"]+=families[i]
         
        families_list = []
        temp={}
        for i in format_families:
            temp["name"]=i
            temp['y']=format_families[i]
            families_list.append(temp)
            temp={}

        viruses_list = []
        ss={'y': (sum_ss/sum_all_viruses), 'color':'#90ed7d', 'drilldown':{"name":"ssRNA","categories":[key for key in ss_viruses.keys()], "data":[value for value in ss_viruses.values()]}}
        ds={'y': (sum_ds/sum_all_viruses), 'color':'#7cb6ec', 'drilldown':{"name":"dsRNA","categories":[key for key in ds_viruses.keys()], "data":[value for value in ds_viruses.values()]}}
        other={'y': (sum_other/sum_all_viruses),'color':'#f45b5c', 'drilldown':{"name":"Other","categories":[key for key in other_viruses.keys()], "data":[value for value in other_viruses.values()]}}
        viruses_list.append(ss)
        viruses_list.append(ds)
        viruses_list.append(other)


        print("\nSTATS\ntotal:",total,"\nSRA and inv:",SRA_count, INV_count,"\nSeqs:",viral_seq,"\n",families_list)
        print(viruses_list)
        
        #Data to send to front-end
        data = {"total":total,"SRA_count":SRA_count,"INV_count":INV_count,"viral_seq_count":viral_seq,"families":families_list, "viruses":viruses_list}
        
        return Response(data, content_type='text')