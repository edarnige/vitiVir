from django.shortcuts import render
#from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
#from rest_framework.response import Response

#from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
#from django_filters.rest_framework import FilterSet, filters
#import rest_framework_filters as filters
#import django_filters


from .serializers import EntrySerializer
from .models import Entry
from .filters import EntrySearchFilter

from rest_framework import pagination

#from rest_framework.settings import api_settings
from rest_framework_csv.renderers import CSVRenderer
from django.db.models import Q


class EntryListView(viewsets.ModelViewSet):
    ''' Entry API list view '''
    
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    pagination_calss= pagination.PageNumberPagination

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('virus_type','sample')


class EntryListCSVExportView(viewsets.ModelViewSet):
    '''Make CSV from Entry list results'''

    queryset = Entry.objects.all()
    #queryset = Entry.objects.filter(Q(sample__icontains="SRR") & Q(virus_type='')).order_by('sample')#('date_joined', '-last_login')
    
    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    pagination_class = None

    renderer_classes = [CSVRenderer]





    '''SCRATCH - in progress'''

    # @action(methods=['get'], detail=False)
    # def get_queryset(self, sample, host_organism, virus_type, verified, exclude_vitis, order):

    #     orderfields = ["-evalue", "query_length", "percent_id"]
    #     queryset = Entry.objects.filter(Q(sample__icontains=sample) & Q(host_organism=host_organism) 
    #         & Q(virus_type=virus_type) & Q(verified=verified) & Q(exclude_vitis=exclude_vitis))
    #     if order in orderfields:
    #         queryset += ".order_by('" + order + "')"

    #     #queryset = Entry.objects.filter(Q(sample__icontains="SRR") & Q(virus_type='')).order_by('sample')#('date_joined', '-last_login')
    #     return queryset


    # def get(self, request):
    #     queryset = Entry.objects.all()
    #     serializer = EntrySerializer(queryset, many=True)
    #     return Response(serializer.data, 
    #                     headers={'Content-Disposition': 'attachment; filename=result.csv'})


    # def get_renderer_context(self):
    #     context = super().get_renderer_context()
    #     import pdb
    #     pdb.set_trace()
    #     print(context)
    #     context['header'] = (
    #        self.request.GET['fields'].split(',')
    #        if 'fields' in self.request.GET else None)
    #     return context





