from django.urls import path

from user.views import AuthenticateUser, UserList


urlpatterns = [
  path('', UserList.as_view(), name='users'),
  path('login', AuthenticateUser.as_view(), name='login'),
]
