from rest_framework import viewsets

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializers import MyUserSerializer
from .models import MyUser
from virData_app.views import EntryListView

from django_filters import rest_framework as filters


class UserViewSet(viewsets.ModelViewSet):
    ''' Manage and create users at /users/manageusers/'''
    
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (AllowAny,) #(permissions.UpdateUser,) #can add multiple classes to viewset

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('email',)

    # @action(detail=True, methods=['put'], name='Change Password')
    # def password(self, request, pk=None):
    #     """Update the user's password."""
    #     ...


class LoginViewSet(viewsets.ViewSet):
    '''Checks email and password, returns authtoken at /users/login/'''

    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        '''Use the ObtainAuthToken APIView to validate and create token'''
        
        token = ObtainAuthToken().post(request)
        return token


class BlastViewSet(viewsets.ViewSet):
    '''place holder'''
    def list(self, request):
        queryset = MyUser.objects.all()
        serializer = MyUserSerializer(queryset, many=True)
        return Response(serializer.data)

    # @action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
    # def blast(self):
    #     '''blast here?'''
#http://biopython.org/DIST/docs/tutorial/Tutorial.html
#7.2.2