from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    ''' Serializer for user objects '''

    class Meta:
        model = MyUser
        fields = ('email','password')
        extra_kwargs = {'password': {'write_only': True, 'required':True}}
    
    def create(self, validated_data):
        ''' Create and return a new user ''' 

        user =MyUser.objects.create(**validated_data)
        Token.objects.create(user=user)
        #print(">>>>>>",user.auth_token, dir(user)) #debug

        return user




