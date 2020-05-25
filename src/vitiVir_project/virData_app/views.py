from django.shortcuts import render, get_object_or_404
from collections import OrderedDict
from django.core.paginator import Paginator as DjangoPaginator

import datetime
import re
import uuid

from rest_framework import viewsets, status, pagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

from rest_framework_csv.renderers import CSVRenderer

from .serializers import EntrySerializer
from .models import Entry



class CustomPaginator(DjangoPaginator):
    @property
    def count(self):
        return self.object_list.length


class CustomMongoPaginator(pagination.PageNumberPagination):

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = CustomPaginator(queryset, page_size)
        self.paginator = paginator
        self.page = self.paginator.page(1)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return queryset

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_next_link(self):

        url = self.request.build_absolute_uri()
        page_number = int(self.request.GET.get('page', 1)) + 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):

        url = self.request.build_absolute_uri()
        page_number = int(self.request.GET.get('page', 1)) - 1
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)


class EntryListView(viewsets.ModelViewSet):
    ''' Entry API list view '''
    
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class= CustomMongoPaginator #pagination.PageNumberPagination

    def get_queryset(self):
        fields = ['sample', 'host_organism', 'virus_type', 'taxonomy', 'description',
            'verified','exclude_vitis', 'start_date', 'end_date', 'ordering']
        mongo_query = []
        order = []
        mongo_results = ''
        entry_ids = []
        queryset = None

        #IN PROGRESS - get detail without going through all the rest....
        if 'pk' in self.kwargs:
            print("pk in kwargs")
            pk_entry = self.kwargs['pk']
            #return Entry.objects.get_object_or_404(pk=pk_entry) 
            return Entry.objects.filter(entry_id=pk_entry) #return all might be faster, to test
        

        if "csv" in self.request.path_info:
            make_csv = True
        else:
            make_csv = False
        
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
            count = mongo_results.count()
        elif mongo_query and not order:
            print("mongo query and no order")
            mongo_results = Entry.objects.mongo_find({'$and': mongo_query})
            count = mongo_results.count()
        elif not mongo_query and order:
            print("no mongo query and yes order")
            mongo_results = Entry.objects.mongo_find().sort(order)
            count = mongo_results.count()
        else:
            print("no mongo query no order")
            queryset = Entry.objects.all()
            count = queryset.count()

        print("count ", count)
        print("make list")
        
        #Make a list of entry ids from mongodb query to make queryset
        page_size = 25
        #only get 25 results at a time 
        try:
            page = int(self.request.GET.get('page'))
        except:
            page= 1 
        start = (page - 1) * page_size
        end = page * page_size

        if make_csv == False:
            for entry in mongo_results[start: end]:
                try: #there are some inviceb with no rps, temp fix to overcome missing entry_ids
                    entry_ids.append(entry['entry_id']) #cursor
                except:
                    print("missing")

            if queryset:
                for entry in queryset[start:end]:
                    try:
                        entry_ids.append(entry.entry_id)  #queryset
                    except:
                        print("missing")

        if make_csv == True:
            for entry in mongo_results:
                try: #there are some inviceb with no rps, temp fix to overcome missing entry_ids
                    entry_ids.append(entry['entry_id']) #cursor
                except:
                    print("missing")


        #print(mongo_results)
        print("entries",len(entry_ids))
        print("list done")
        
        #second query and sorting
        if entry_ids:
            queryset = Entry.objects.filter(entry_id__in = entry_ids)
            if make_csv == False and order: #do not bother to order csv
                print("ordering...")
                queryset= L(sorted(queryset, key=lambda i: entry_ids.index(i.pk)))
        if not entry_ids and mongo_query: #if there are no results when filtering
            queryset=L([])

        print("queryset ready")
        queryset.length = count
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

    def get_queryset(self):
        return EntryListView.get_queryset(self)


class L(list):
    """
    A subclass of list that can accept additional attributes.
    Used just like a regular list.
    http://code.activestate.com/recipes/579103-python-addset-attributes-to-list/
    """
    def __new__(self, *args, **kwargs):
        return super(L, self).__new__(self, args, kwargs)

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            list.__init__(self, args[0])
        else:
            list.__init__(self, args)
        self.__dict__.update(kwargs)

    def __call__(self, **kwargs):
        self.__dict__.update(kwargs)
        return self