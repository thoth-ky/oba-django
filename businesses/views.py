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
    if business not in  self.request.user.businesses.all():
      raise PermissionDenied
    else:
      self.permission_classes = [IsAuthenticated,]
    return super(BusinessTransactions, self).get_permissions()
  

  def get(self, *args, **kwargs):
    business = get_object_or_404(Business, id=self.kwargs.get('pk'))
    date_range = ['2020-01-01', '2020-12-31']
    total_orders = business.transactions.filter(
      transaction_date__range=date_range, transaction_type='Order'
      ).aggregate(Sum('total_transaction_amount'))
    total_order_payments = business.transactions.filter(
      transaction_date__range=date_range, transaction_type='Order payment'
      ).aggregate(Sum('total_transaction_amount'))
    
    total_bills = business.transactions.filter(
      transaction_date__range=date_range, transaction_type='Bill'
      ).aggregate(Sum('total_transaction_amount'))
    total_bill_payments = business.transactions.filter(
      transaction_date__range=date_range, transaction_type='Bill Payment'
      ).aggregate(Sum('total_transaction_amount'))
    
    return Response({
      'amount_in': total_orders.get('total_transaction_amount__sum') or 0 - total_order_payments.get('total_transaction_amount__sum') or 0,
      'bills_due': total_bills.get('total_transaction_amount__sum') or 0 - total_bill_payments.get('total_transaction_amount__sum') or 0
    })

