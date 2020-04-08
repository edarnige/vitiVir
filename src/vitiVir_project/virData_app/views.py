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



class SampleView(APIView): 
    ''' Handles sample view at /api/data/<sample> '''

    def get(self, request, sample, format=None):
        ''' Show list of entries from same sample  '''
        print(">>>",sample) #ok
        entries = models.Entry.objects.all()
        serializer = serializers.EntrySerializer(entries, many=True)
        sample = get_object_or_404(models.Entry, sample=sample) #filter? sample is not pk
        entry_data = serializer.data
        
        return Response({"entries":entry_data, "sample":sample}) #stock.data?

    def post(self, request):
        ''' Create an entry '''

        serializer = serializers.EntrySerializer(data=request.data)

        if serializer.is_valid():
            entry = serializer.data.get()
    
            return Response({'New entry': entry})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntryView(APIView):
    ''' Handles single entry view at /api/data/<sample>/<entry_id> '''

    def get(self, request, sample, entry_id, format=None):
        ''' Show entry detail '''
        print(">>>",sample, entry_id) #ok
        entries = models.Entry.objects.all()
        serializer = serializers.EntrySerializer(entries, many=True)
        #sample = get_object_or_404(models.Entry, sample=sample) #filter? sample is not pk
        entry = get_object_or_404(models.Entry, entry_id=entry_id)
        entry_data = serializer.data
        
        return Response({"entries":entry_data, "entry":entry}) #stock.data?

    def post(self, request):
        ''' Create an entry '''

        serializer = serializers.EntrySerializer(data=request.data)

        if serializer.is_valid():
            entry = serializer.data.get()
    
            return Response({'New entry': entry})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


