from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from . import serializers
from . import models
from . import permissions 


class UserListView(generics.ListAPIView):
    ''' List all users '''

    serializer = serializers.MyUserSerializer
    queryset = models.MyUser.objects.all()
    #authentication_classes = (TokenAuthentication,) #session authentication cookies? 
    #permission_classes = (permissions.UpdateUser,) #can add multiple classes to viewset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.MyUserSerializer(queryset, many=True)

        return Response(serializer.data)


class UserView(APIView):
    ''' Handles creating, reading, and updating users ar /api/user/<user_id> '''


    def get(self, request, user_id):
        user = get_object_or_404(models.MyUser, user_id=user_id)
        serializer = serializers.MyUserSerializer(user)
        user_data = serializer.data 

        return Response(user_data) 

    def post(self, request):
        ''' Create a user '''
  
        serializer = serializers.MyUserSerializer(data=request.data)

        if serializer.is_valid():
            user_saved = serializer.save()
            return Response({'Success new user': user_saved})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
