from django.shortcuts import render
#from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

#from rest_framework.filters import SearchFilter, OrderingFilter
#from django_filters import rest_framework as filters
#from django_filters.rest_framework import FilterSet, filters
#import rest_framework_filters as filters
#import django_filters


from .serializers import EntrySerializer
from .models import Entry
from .filters import EntrySearchFilter


class EntryListView(viewsets.ModelViewSet):
    ''' Entry API list view '''
    
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
