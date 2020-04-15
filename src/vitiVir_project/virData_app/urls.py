from django.urls import path
from django.conf.urls import include 

# from rest_framework.routers import DefaultRouter
# from rest_framework import routers

from . import views

urlpatterns = [
    path('data/entries',views.EntryListView.as_view()),
    #path('data/<str:sample>',views.SampleListView.as_view()), #remove ?
    path('data/<str:sample>/<str:entry_id>',views.EntryDetailView.as_view()),
]

# /api/data/<sa1
# SRR1051000_2
# SRR1051000_2

# /api/data/<sample>/<entry_id>
# SRR1051000_1:
#   blastx:
#   rpsblast:
#   metadata:

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