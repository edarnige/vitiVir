from django.urls import path
from django.conf.urls import include 

# from rest_framework.routers import DefaultRouter
from rest_framework import routers

from .views import EntryListView, EntryListCSVExportView, EntryListFastaExportView

router= routers.DefaultRouter()
router.register('entries', EntryListView)
router.register('entries_csv', EntryListCSVExportView,'entries-csv')
router.register('entries_fasta', EntryListFastaExportView, 'entries-fasta')

urlpatterns = [
    path('', include(router.urls)),
]



# /api/data/entry/<sample>?balststrps.evalue=-2

# sample= 1
# sample2
# sample 3

# post query
# request
# {
#     "filters": [
#       {
#         "field_names": “balsxtrpx.evalue”,
#         "value": “1233”
#       },
#  {
#         "field_names": “balsxtrpx.frame”,
#         "value": “-2”
#       }
    
#     ]
#   }

#   ordering_fields = [‘ballstx.epx’, ‘query_id’]

#test
#SRR10518885
#12a3732d-65ae-4e59-9364-7d7c2848e77c