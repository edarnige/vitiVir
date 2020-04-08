from django.urls import path
from django.conf.urls import include 

# from rest_framework.routers import DefaultRouter
# from rest_framework import routers

from . import views

urlpatterns = [
    path('data/entries/',views.EntryListView.as_view()),
    path('data/entry/<str:sample>',views.SampleView.as_view()), #remove /entry?
    path('data/entry/<str:sample>/<str:entry_id>',views.EntryView.as_view()), #remove /entry?
]

# /api/data/<sample>
# SRR1051000_1
# SRR1051000_2
# SRR1051000_2

# /api/data/<sample>/<entry_id>
# SRR1051000_1:
#   blastx:
#   rpsblast:
#   metadata:

