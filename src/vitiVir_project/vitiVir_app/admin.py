from django.contrib import admin
from .models import MyUser, MyUserManager

# Register your models here to Django /admin
admin.site.register(MyUser)