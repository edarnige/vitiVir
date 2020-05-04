from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from .views import UserViewSet, LoginViewSet

router= routers.DefaultRouter()
router.register('manageusers', UserViewSet)
router.register('login', LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]