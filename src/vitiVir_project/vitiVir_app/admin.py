from django.contrib import admin
from .models import UserProfile, UserProfileManager

# Register your models here to Django /admin
admin.site.register(UserProfile)