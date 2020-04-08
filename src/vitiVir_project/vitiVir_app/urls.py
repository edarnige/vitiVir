from django.urls import path
from django.conf.urls import include 

# from rest_framework.routers import DefaultRouter
# from rest_framework import routers

from . import views



urlpatterns = [
    path('users/',views.UserListView.as_view()),
    path('user/',views.UserView.as_view()),
]