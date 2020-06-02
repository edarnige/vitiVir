import os, glob
from django.utils import timezone
from rest_framework import viewsets

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializers import MyUserSerializer
from .models import MyUser
from virData_app.views import EntryListView

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

        with open(tmp_file_path, 'w') as f:
            f.write(data)

        blastn_path = '/vagrant/db/blastdb/ncbi-blast-2.10.0+/bin/' + type_of_blast
        
        if type_of_blast == 'blastn':
            blast_cline = NcbiblastnCommandline(
                cmd=blastn_path, 
                query=tmp_file_path, 
                db='/vagrant/db/blastdb/vitiVirSeq.fasta', 
                outfmt=5, 
                out=tmp_out_file_path)
            blast_cline
            stdout, stderr = blast_cline()
        elif type_of_blast == 'tblastn':
            blast_cline = NcbitblastnCommandline(
                cmd=blastn_path, 
                query=tmp_file_path, 
                db='/vagrant/db/blastdb/vitiVirSeq.fasta', 
                outfmt=5, 
                out=tmp_out_file_path)
            blast_cline
            stdout, stderr = blast_cline()
        elif type_of_blast == 'tblastx':
            blast_cline = NcbitblastxCommandline(
                cmd=blastn_path, 
                query=tmp_file_path, 
                db='/vagrant/db/blastdb/vitiVirSeq.fasta', 
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
    
    
    #evalue_threshold = 1e-10 #handeled in front ? 
    #max_output = None

