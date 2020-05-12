from django.shortcuts import render
#from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
#from rest_framework.response import Response

#from rest_framework.filters import SearchFilter, OrderingFilter
#from django_filters import rest_framework as filters
#from django_filters.rest_framework import FilterSet, filters
#import rest_framework_filters as filters
#import django_filters


from .serializers import EntrySerializer
from .models import Entry
from .filters import EntrySearchFilter

from rest_framework import pagination

from rest_framework_csv.renderers import CSVRenderer
from django.db.models import Q

from bson.json_util import dumps


class EntryListView(viewsets.ModelViewSet):
    ''' Entry API list view '''
    
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    #filter_class = EntrySearchFilter
    pagination_calss= pagination.PageNumberPagination

    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('virus_type','sample') 

    def get_queryset(self):
        fields = ['query_length', 'organism']
        queryset = self.queryset
        for field in fields:
            
            #Get from url ?organism=Vitis vinifera
            if field in self.request.GET:
                value = self.request.GET.get(field)
                if field == 'query_length':
                    queryset = queryset.filter(blastx__exact={'query_length': int(value)})
                elif field == 'organism':
                    queryset = queryset.filter(blastx__exact={'organism': value})

        # ordering not working
        ordering = self.request.GET.get('ordering')

        if ordering:
            queryset = queryset.order_by(ordering)
        print(queryset.query)
        return queryset

class EntryListCSVExportView(viewsets.ModelViewSet):
    '''Make CSV from Entry list results'''

    queryset = Entry.objects.all()
    #use self.request.GET ^ to get all params from url passed
    #queryset = Entry.objects.filter(Q(sample__icontains="SRR") & Q(virus_type='')).order_by('sample')#('date_joined', '-last_login')

    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    pagination_class = None

    renderer_classes = [CSVRenderer]





    '''SCRATCH - in progress'''

    # @action(methods=['get'], detail=False)
    # def get_queryset(self, sample, host_organism, virus_type, verified, exclude_vitis, order):
            #use kwargs from url? 
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





