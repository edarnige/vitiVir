from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters import rest_framework as filters
#from django_filters.rest_framework import FilterSet, filters 
#import rest_framework_filters as filters
#import django_filters


from virData_app.serializers import EntrySerializer
from virData_app.models import Entry
from virData_app.filters import EntrySearchFilter


class EntryListView(generics.ListAPIView):
    ''' Entry API list view '''
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    #print("\n>>>>>>",queryset[0].blastx.organism,"\n")

    # def get_queryset(self):
    #     queryset = Entry.objects.all()
    #     return queryset

    #filter_backends = (filters.OrderingFilter)
    #filter_backends = (filters.DjangoFilterBackend,)
    #filter_fields = ('virus_type','blastx__organism',)
    #ordering_fields = ['blastx__.query_length',]# 'blastx__percent_identity', 'blastx__evalue']
    #filterset_fields = ['sample','verified','host_organism','virus_type',] #'blastx__organism'

    #paginate_by = 5
    
    filterset_class = EntrySearchFilter #from filters.py

    #No need for list method... 
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = EntrySerializer(self.queryset, many=True)
    #     return Response(serializer.data)

    #post





class SampleListView(generics.ListAPIView): 
    ''' Handles sample view at /api/data/<sample> '''
    
    serializer_class = EntrySerializer

    def get_queryset(self):
        queryset = Entry.objects.filter(sample=self.sample)
        return queryset

    def list(self, request, sample, format=None):
        ''' Show list of entries from same sample  '''
        self.sample =sample
        queryset = self.get_queryset()
        serializer = EntrySerializer(queryset, many=True)
        return Response(serializer.data) 


class EntryDetailView(APIView):
    ''' Handles single entry view at /api/data/<sample>/<entry_id> '''

    def get(self, request, sample, entry_id, format=None):
        ''' Show entry detail '''
        print(">>>",sample, entry_id) #ok
        entry = get_object_or_404(Entry, sample=sample, entry_id=entry_id) #filter? sample is not pk
        serializer = EntrySerializer(entry)
        entry_data = serializer.data

        return Response(entry_data)  # serializer.data

    def put(self, request):
        pass


    def post(self, request):
        ''' Create an entry '''

        serializer = EntrySerializer(data=request.data)

        if serializer.is_valid():
            entry = serializer.data.get()
    
            return Response({'New entry': entry})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


