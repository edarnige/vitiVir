from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from . import serializers
from . import models


class EntryListView(generics.ListAPIView):
    ''' Entry API view '''

    queryset = models.Entry.objects.all()
    
    serializer_class = serializers.EntrySerializer

    def list(self, request):
        queryset = self.get_queryset()
        print("\n",queryset[1000],"\n") #ok 
        print("\n>>>>>>",self.queryset[0].blastx.query_length,"\n")
        serializer = serializers.EntrySerializer(queryset, many=True)

        return Response(serializer.data)



class SampleListView(generics.ListAPIView): 
    ''' Handles sample view at /api/data/<sample> '''
    
    serializer_class = serializers.EntrySerializer

    def get_queryset(self):
        queryset = models.Entry.objects.filter(sample=self.sample)
        return queryset

    def list(self, request, sample, format=None):
        ''' Show list of entries from same sample  '''
        self.sample =sample
        queryset = self.get_queryset()
        serializer = serializers.EntrySerializer(queryset, many=True)
        return Response(serializer.data) #stock.data?
    
    def post(self, request):
        print(">>>>>",request)
        pass



class EntryView(APIView):
    ''' Handles single entry view at /api/data/<sample>/<entry_id> '''

    def get(self, request, sample, entry_id, format=None):
        ''' Show entry detail '''
        print(">>>",sample, entry_id) #ok
        entry = get_object_or_404(models.Entry, sample=sample, entry_id=entry_id) #filter? sample is not pk
        serializer = serializers.EntrySerializer(entry)
        entry_data = serializer.data
        
        return Response(serializer.data) #stock.data?

    def post(self, request):
        ''' Create an entry '''

        serializer = serializers.EntrySerializer(data=request.data)

        if serializer.is_valid():
            entry = serializer.data.get()
    
            return Response({'New entry': entry})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


