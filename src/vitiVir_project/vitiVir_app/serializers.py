from rest_framework import serializers
#Tokens?

from . import models


class MyUserSerializer(serializers.ModelSerializer):
    ''' Serializer for user objects '''

    class Meta:
        model = models.MyUser
        fields = '__all__' #('user_id','email','password') #flags?
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        ''' Create and return a new user ''' 

        user = models.MyUser(
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user




