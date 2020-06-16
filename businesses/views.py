from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from businesses.models import Business
from businesses.serializers import BusinessSerializer

class BusinessList(generics.ListCreateAPIView):
  permission_classes =( IsAuthenticated,)
  serializer_class = BusinessSerializer
  queryset = Business.objects.all()

  
  def get_permissions(self):
    method = self.request.method
    if method == 'GET':
      self.permission_classes = [IsAdminUser,]
    else:
      self.permission_classes = [IsAuthenticated,]

    return super(BusinessList, self).get_permissions()

class BusinessDetails(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = BusinessSerializer
  permission_classes =(IsAuthenticated,)

  def get_object(self):
    if self.request.user.is_superuser:
      return get_object_or_404(Business, id=self.kwargs.get('pk'))
    else:
      return get_object_or_404(Business, id=self.kwargs.get('pk'), owner=self.request.user)