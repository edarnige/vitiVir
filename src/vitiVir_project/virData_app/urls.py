from django.urls import path
from django.conf.urls import include 

from rest_framework import routers

from .views import EntryListView, EntryListCSVExportView, EntryListFastaExportView

router= routers.DefaultRouter()
router.register('entries', EntryListView)
router.register('entries_csv', EntryListCSVExportView,'entries-csv')
router.register('entries_fasta', EntryListFastaExportView, 'entries-fasta')

urlpatterns = [
    path('', include(router.urls)),
]