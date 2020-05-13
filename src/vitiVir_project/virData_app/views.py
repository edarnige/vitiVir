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

#import re



class EntryListView(viewsets.ModelViewSet):
    ''' Entry API list view '''
    
    queryset = Entry.objects.all()
    #queryset = Entry.objects.mongo_find({'sample':'SRR10518885'})
    #print(">>>>>>",queryset)

    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_calss= pagination.PageNumberPagination


    # cursor = Entry.objects.mongo_find({'blastx.organism':{'$regex':'vitis', '$options': 'i'}})
    # print(cursor)
    # count =0
    # entry_ids=[]
    # for i in cursor:
    #     count+=1
    #     entry_ids.append(i['entry_id'])

    # print(count)
    # print(entry_ids)

    # queryset = Entry.objects.filter(entry_id__in=entry_ids)
    # print(">>>2>>>",queryset)


    def get_queryset(self):
        fields = ['sample', 'host_organism', 'virus_type', 'taxonomy', 'description','verified','exclude']
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
                # if field == 'exclude':
                #     mongo_query.append({'organism':{'$not':{'$regex':value, '$options': 'i'}}})
                #dates       
        
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




    # def get_queryset(self):
    #     fields = ['query_length', 'organism', 'sample']
    #     queryset = self.queryset
    #     #query={'blastx__startswith':{'organism':'Vitis vinifera'}}
    #     for field in fields:
            
    #         #Get from url ?organism=Vitis vinifera
    #         if field in self.request.GET:
    #             value = self.request.GET.get(field)
    #             if field == 'query_length':
    #                 #queryset = queryset.filter(blastx__exact={'query_length': int(value)})

    #             elif field == 'organism':
    #                 queryset = queryset.mongo_find({'blastx':{'organism':{'$regex':"*"+value+"*"}}})
    #             # elif field == 'sample':
    #             #     #queryset = queryset.filter(sample__icontains=value)
    #             #     queryset = queryset.mongo_find({'sample':{'$regex':"*"+value+"*"}})


    #     # ordering not working
    #     ordering = self.request.GET.get('ordering')

    #     if ordering:
    #         queryset = queryset.order_by(ordering)
        
    #     #queryset = queryset.filter(**query)
    #     print(queryset.query)
    #     return queryset

        #     index = [i for i in queryset.mongo_aggregate([
        #     {
        #         '$match': {
        #             'headline': self.kwargs['path']
        #         }
        #     },
        # ])]




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

    #Filtering idea
#     $(".filterInput").each(function() {
#     var column_name = $(this).attr("name")
#     filters[column_name] = $(this).val();
# });

# query = {}
# for k, v in filters.items():
#     if v:
#         query[k + '__icontains'] = v

# result = model.objects.filter(**query).order_by(order_by).skip(page_size*(page-1)).limit(page_size).only(*attr_names)


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





