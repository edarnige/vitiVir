from django.core.mail import send_mail
from django.conf import settings

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    ''' Serializer for user objects '''

    class Meta:
        model = MyUser
        fields = ('email','password', 'can_verify')
        extra_kwargs = {'password': {'write_only': True, 'required':True}}
    
    def create(self, validated_data):
        ''' Create and return a new user ''' 

        user = MyUser(
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        #user =MyUser.objects.create(**validated_data)

        #Token.objects.create(user=user)
        #print(">>>>>>",user.auth_token, dir(user)) #debug

        return user


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    message = serializers.CharField()

    def send(self):
        return send_mail(
            "Contact from VitiVir", 
            'Message sent to VitiVir from '+self.validated_data['name']+':\n'+self.validated_data['message'], 
            settings.EMAIL_HOST_USER, #from host
            [settings.EMAIL_HOST_USER, self.validated_data['email'], 'eden.darnige@inrae.fr'] #to host, client, and my work email   #marie.lefebvre@inrae.fr
        )
