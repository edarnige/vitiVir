from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import pagination
from rest_framework.response import Response

from .serializers import EntrySerializer
from .models import Entry
from .filters import EntrySearchFilter

from rest_framework_csv.renderers import CSVRenderer

import datetime

from bson.json_util import dumps



class EntryListView(viewsets.ModelViewSet):
    ''' Entry API list view '''
    
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_calss= pagination.PageNumberPagination

    #queryset = Entry.objects.filter(blastx__query_length=7005)

    def get_queryset(self):
        fields = ['sample', 'host_organism', 'virus_type', 'taxonomy', 'description',
            'verified','exclude_vitis', 'start_date', 'end_date', 'ordering']
        mongo_query = []
        order = []
        mongo_results = ''
        entry_ids = []
        
        #Get all fields and values passed from frontend (elif?)
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
                    if value != "NaN-NaN-NaN":
                        try: #in case of misentry
                            startdate = datetime.datetime.strptime(value,'%Y-%m-%d')
                            mongo_query.append({'$or':[
                                {'sra_metadata.ReleaseDate':{'$gte':startdate}}, 
                                {'inv_metadata.date':{'$gte':startdate}}
                            ]})
                        except:
                            pass
                if field == 'end_date':
                    if value != "NaN-NaN-NaN":
                        try:
                            enddate = datetime.datetime.strptime(value,'%Y-%m-%d')
                            mongo_query.append({'$or':[
                                {'sra_metadata.ReleaseDate':{'$lte':enddate}}, 
                                {'inv_metadata.date':{'$lte':enddate}}
                            ]})
                        except:
                            pass
                if field == 'ordering':
                    if value == 'evalue':
                        order.append(('blastrps.evalue', 1)) 
                    if value == 'query_length':
                        order.append(('blastx.query_length', -1))
                    if value == 'percent_id':
                        order.append(('blastx.percent_identity', -1))

        #Which type of mongo query    
        if mongo_query and order:
            print("mongo query and order")
            mongo_results = Entry.objects.mongo_find({'$and': mongo_query}).sort(order)
        elif mongo_query and not order:
            print("mongo query and no order")
            mongo_results = Entry.objects.mongo_find({'$and': mongo_query})
        elif not mongo_query and order:
            print("no mongo query and yes order")
            #Entry.objects.mongo_createIndex({order[0][0]:order[0][1]})
            mongo_results = Entry.objects.mongo_find().sort(order)
        else:
            print("no mongo query no order")
            queryset = Entry.objects.all()

        #Make a list of entry ids from mongodb query to make queryset
        count = 0
        print("make list")
        for entry in mongo_results:
            try: #there are some inviceb with no rps, temp fix to overcome missing entry_ids
                entry_ids.append(entry['entry_id'])
                count+=1
                #print(count)
            except:
                pass
        #print(mongo_results)
        print("list done")
        
        if entry_ids:
            queryset = Entry.objects.filter(entry_id__in = entry_ids)
            print(type(queryset[0]))
            queryset = sorted(queryset, key=lambda i: entry_ids.index(i.pk))
        print("queryset ready")
        
        return queryset

    def partial_update(self, request, *args, **kwargs):
        ''' Patch many based on sample or query_id '''
        instance = self.queryset.get(pk=kwargs.get('pk'))
        query_id = instance.query_id #contig for verified and virus type
        sample = instance.sample #sample for host org
        data=request.data

        #update directly in the mongodb
        Entry.objects.mongo_update_many({'query_id': query_id},{'$set':{'verified':data['verified'], 'virus_type':data['virus_type']}}, upsert=True) 
        Entry.objects.mongo_update_many({'sample': sample},{'$set':{'host_organism':data['host_organism']}}, upsert=True)
        
        return Response()
        



class EntryListCSVExportView(viewsets.ModelViewSet):
    '''Make CSV from Entry list results'''

    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    renderer_classes = [CSVRenderer]

    def get_queryset(self): #repeats long search -other way?
        return EntryListView.get_queryset(self)
