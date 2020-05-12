from virData_app.models import Entry, Blastx, Blastrps, SRAMetadata#, INVMetadata

#from django_filters import rest_framework as filters

import rest_framework_filters as filters
import django_filters


"""
class SRAMetaFilter(filters.FilterSet):
    class Meta:
        model = SRAMetadata
        fields = ['ReleaseDate',]
        #range of dates...
        #date__gt = django_filters.NumberFilter(field_name="ReleaseDate", lookup_expr='')
        #date__lt


# class SRAMetaFilter(filters.FilterSet):
#     class Meta:
#         fields = ['ReleaseDate',]


class BlastrpsFilter(filters.FilterSet):
    class Meta:
        model = Blastrps
        fields = ['evalue',]


class BlastxFilter(filters.FilterSet):
    #organism = filters.BooleanFilter(field_name='organism',lookup_expr="Vitis vinifera")
    class Meta:
        model = Blastx
        fields = ['organism','query_length','percent_identity',]


class EntryFilter(filters.FilterSet):
    blastx = filters.RelatedFilter('BlastxFilter', queryset=Blastx.objects.all())
    sra_metadata = filters.RelatedFilter('SRAMetaFilter', queryset=Blastx.objects.all())
    blastrps = filters.RelatedFilter('BlastrpsFilter', queryset=Blastrps.objects.all())
    #inv_metadata = filters.RelatedFilter('INVMetaFilter', queryset=Blastx.objects.all())
    class Meta:
        model = Entry
        fields = ('sample','verified','host_organism','virus_type')
        #fields = '__all__'
"""

class BlastxFilter(filters.FilterSet):
    #organism = filters.BooleanFilter(field_name='organism',lookup_expr="Vitis vinifera")
    class Meta:
        model = Blastx
        fields = ['organism','query_length','percent_identity', 'taxonomy']

from djongo import models
class EntrySearchFilter(filters.FilterSet):
    #sample = filters.CharFilter(lookup_expr="iexact")
    #inv_metadata = filters.RelatedFilter('INVMetaFilter', queryset=Blastx.objects.all())
    blastx = filters.RelatedFilter('BlastxFilter', queryset=Blastx.objects.all())
    class Meta:
        model = Entry
        fields = ("sample","blastx")
        #fields ={
        #    'sample': ['icontains',],
        #    'host_organism':['icontains'],
        #    'virus_type':['icontains'],
        #    'verified':['exact'],
        #    'blastx': ['exact']

        #}

        #filter_overrides = {
         #   models.EmbeddedField: {
        #        'filter_class': BlastxFilter,
        #        'extra': lambda f: {
        #            'lookup_expr': 'exact',
        #        },
        #    }
        #}
