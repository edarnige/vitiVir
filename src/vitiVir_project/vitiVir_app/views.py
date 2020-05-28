from rest_framework import viewsets

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
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
    ''' Blastn or tblastx against local vitivirseq db at /api/blast/'''

    blastn_path = '/vagrant/db/blastdb/ncbi-blast-2.10.0+/bin/blastn'
    blast_cline = NcbiblastnCommandline(cmd=blastn_path, query='/vagrant/db/blastdb/genes_of_interest.fasta', db='/vagrant/db/blastdb/vitiVirSeq.fasta', outfmt=5, out='/vagrant/db/results2.xml')
    blast_cline
    #print(blast_cline)
    stdout, stderr = blast_cline()
    result_handle = open("/vagrant/db/results2.xml")

    
    #blast_cline= NcbiblastnCommandline(query='PATH/to/genes_of_interest.fasta', db='/PATH/to/local/db/protein.fa', out='PATH/to/results.xml')
    #http://biopython.org/DIST/docs/tutorial/Tutorial.html
    #7.2.2
    #What about if only 1 result? check fasta input ? 
    # blast_records = NCBIXML.parse(result_handle)
    # for blast_record in blast_records:
    #     print(">>>>>ping")
        #convert to json object to send to front
