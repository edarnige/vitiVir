from rest_framework import viewsets

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import MyUserSerializer
from .models import MyUser
from virData_app.views import EntryListView


class UserViewSet(viewsets.ModelViewSet):
    ''' List all users /api/users '''
    
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (AllowAny,) #(permissions.UpdateUser,) #can add multiple classes to viewset


class LoginViewSet(viewsets.ViewSet):
    '''Checks email and password, returns authtoken'''

    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        '''Use the ObtainAuthToken APIView to validate and create token'''
        
        token = ObtainAuthToken().post(request)
        return token
