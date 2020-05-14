from django.shortcuts import render
#from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
#from rest_framework.response import Response

from .serializers import EntrySerializer
from .models import Entry
from .filters import EntrySearchFilter

from rest_framework import pagination

from rest_framework_csv.renderers import CSVRenderer
from django.db.models import Q

import datetime



class EntryListView(viewsets.ModelViewSet):
    ''' Entry API list view '''
    
    queryset = Entry.objects.all()

    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_calss= pagination.PageNumberPagination

    def get_queryset(self):
        fields = ['sample', 'host_organism', 'virus_type', 'taxonomy', 'description','verified','exclude_vitis', 'start_date', 'end_date']
        mongo_query = []
        mongo_results = ''
        entry_ids = []

        for field in fields:
            if field in self.request.GET:
                value = self.request.GET.get(field)
                if field == 'sample':
                    mongo_query.append({'sample':{'$regex':value, '$options': 'i'}})
                if field == 'host_organism':
                    mongo_query.append({'host_organism':{'$regex':value, '$options': 'i'}})
                if field == 'virus_type':
                    mongo_query.append({'virus_type':{'$regex':value, '$options': 'i'}})
                if field == 'taxonomy':
                    mongo_query.append({'blastx.taxonomy':{'$regex':value, '$options': 'i'}})
                if field == 'description':
                    mongo_query.append({'blastrps.description':{'$regex':value, '$options': 'i'}})
                if field == 'verified':
                    if value == 'true':
                        value = True
                        mongo_query.append({'verified':value})
                if field == 'exclude_vitis':
                     if value == 'true':
                        mongo_query.append({'blastx.organism':{'$not':{'$regex':'Vitis vinifera', '$options': 'i'}}})
                if field == 'start_date':
                    try: #in case of misentry
                        startdate = datetime.datetime.strptime(value,'%Y-%m-%d')
                        mongo_query.append({'$or':[
                            {'sra_metadata.ReleaseDate':{'$gte':startdate}}, 
                            {'inv_metadata.date':{'$gte':startdate}}
                        ]})
                    except:
                        pass
                if field == 'end_date':
                    try:
                        enddate = datetime.datetime.strptime(value,'%Y-%m-%d')
                        mongo_query.append({'$or':[
                            {'sra_metadata.ReleaseDate':{'$lte':enddate}}, 
                            {'inv_metadata.date':{'$lte':enddate}}
                        ]})
                    except:
                        pass

        
        for entry in mongo_results:
            entry_ids.append(entry['entry_id'])
        
        if mongo_query:
            mongo_results = Entry.objects.mongo_find({'$and': mongo_query})
            for entry in mongo_results:
                entry_ids.append(entry['entry_id'])
            queryset = Entry.objects.filter(entry_id__in = entry_ids)
        else:
            queryset = Entry.objects.all()

        return queryset



    #     # ordering not working
    #     ordering = self.request.GET.get('ordering')

    #     if ordering:
    #         queryset = queryset.order_by(ordering)
        



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

 