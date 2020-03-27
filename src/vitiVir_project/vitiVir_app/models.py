
# Create your models here.
from djongo import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# User help:
# https://docs.djangoproject.com/en/3.0/ref/contrib/auth/

# Create your models here.

class UserProfileManager(BaseUserManager): #inherit from BaseUserManager
    '''
    Helps Django work with custom user model
    '''

    def create_user(self, email, password):
        ''' Creates a new user profile object '''
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email) #lowercase
        user = self.model(email=email)

        # can verify
        if email == 'thierry.candresse@inrae.fr' or email == 'armelle.marais-colombel@inrae.fr':
            user.can_verify = True

        user.set_password(password)
        user.save(using=self._db) #default db in settings

        return user

    def create_superuser(self, email, password):
        ''' Creates a new superuser '''
        email = self.normalize_email(email)
        user = self.model(email=email)

        user.is_superuser = True
        user.is_staff = True
        user.can_verify = True

        user.set_password(password)
        user.save(using = self._db)

        return user

    

class UserProfile(AbstractBaseUser, PermissionsMixin):
    '''
    Custom user model
    Represents a "user profile" inside the system
    '''

    email = models.EmailField(max_length=255, unique=True, primary_key=True) #No wannnnnt
    #valueerror at /admin/login/ cannot force an update in save() with no primary key
    can_verify = models.BooleanField(default=False) # flag active vs guest user

    is_active = models.BooleanField(default=True) # not sure if will use
    is_staff = models.BooleanField(default=False)
    
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] #email is username field, by default set to required, password too

    # Helper fxns 
    def get_email(self):
        ''' Used to get a user's first name '''
        return self.email

    def __str__(self):
        '''Convert object to string'''
        return self.email

    @property
    def get_can_verify(self):
        ''' Used to determine if user can verify taxo '''
        return self.can_verify

    @property #access via user.get_is_staff
    def get_is_staff(self):
        ''' Used to determine if user is admin and can CRUD '''
        return self.is_staff
