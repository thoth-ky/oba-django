from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Sum

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from businesses.models import Business
from businesses.serializers import BusinessSerializer

class BusinessList(generics.ListCreateAPIView):
  serializer_class = BusinessSerializer
  queryset = Business.objects.all()
  permission_classes = [IsAuthenticated, ]

  def get_queryset(self):
    if self.request.user.is_superuser:
      return Business.objects.all()
    return Business.objects.filter(owner=self.request.user)

class BusinessDetails(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = BusinessSerializer
  permission_classes =(IsAuthenticated,)

  def get_object(self):
    if self.request.user.is_superuser:
      return get_object_or_404(Business, id=self.kwargs.get('pk'))
    else:
      return get_object_or_404(Business, id=self.kwargs.get('pk'), owner=self.request.user)


class BusinessTransactions(generics.RetrieveAPIView):
  def get_permissions(self):
    business = get_object_or_404(Business, id=self.kwargs.get('pk'))
    if business not in  self.request.user.businesses.all() and not self.request.user.is_superuser:
      raise PermissionDenied
    else:
      self.permission_classes = [IsAuthenticated,]
    return super(BusinessTransactions, self).get_permissions()
  

  def get(self, *args, **kwargs):
    # get business
    business = get_object_or_404(Business, id=self.kwargs.get('pk'))

    # get params
    start_date = self.request.GET.get('from') or self.kwargs['from']
    end_date = self.request.GET.get('to') or self.kwargs['to']
    date_range = [start_date, end_date]

    # get summaries
    cash_flow = business.cash_flow(date_range)
    top_five_by_quantity = business.top_five_items_by_quantity(date_range)
    top_five_by_value = business.top_five_items_by_value(date_range)
    
    return Response({
      'cash_flow': cash_flow,
      'top_five_by_quantity': top_five_by_quantity,
      'top_five_by_value': top_five_by_value,
    })

