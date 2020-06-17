from rest_framework import generics, mixins
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response


from user.serializers import UserSerializer, AuthSerializer
from user.models import User

class UserList(generics.ListCreateAPIView):

  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_permissions(self):
    method = self.request.method
    if method == 'GET':
      self.permission_classes = [IsAdminUser,]
    else:
      self.permission_classes = [AllowAny,]

    return super(UserList, self).get_permissions()


class AuthenticateUser(APIView):
  serializer_class = AuthSerializer

  def post(self, request, format=None):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.validated_data['user']
      token, created = Token.objects.get_or_create(user=user)

      return Response({
        'username': user.username,
        'email': user.email,
        'token': token.key,
        'user_id': user.id,
        'created': created,
      })
    return Response({
      'errors': serializer.errors,
    })
