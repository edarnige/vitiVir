from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from .views import UserViewSet, LoginViewSet, BlastViewSet

router= routers.DefaultRouter()
router.register('users/manageusers', UserViewSet)
router.register('users/login', LoginViewSet, basename='login')
router.register('api/blast', BlastViewSet, basename='blast')

urlpatterns = [
    path('', include(router.urls)),
]