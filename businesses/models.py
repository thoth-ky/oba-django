from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django_countries.fields import CountryField
from user.models import User


REVENUE_RANGE = (
  (1, 'Below KeS 50,000'),
  (2, 'KeS 50,000 - KeS 150,000'),
  (3, 'KeS 150,000 - KeS 300,000'),
  (4, 'KeS 300,000 - KeS 500, 000'),
  (5, 'Above KeS 500,000')
)
ENTITY_CHOICES = (('R', 'Retailer'), ('S', 'Supplier'))

ACCOUNTS_SOFTWARE = (('QB', 'Quickbooks'), ('EX', 'Excel SpreadSheets'))

class Business(models.Model):
  owner = models.ForeignKey(User, related_name='businesses', on_delete=models.CASCADE)
  name = models.CharField(max_length=25, help_text='Name of business')
  business_abbreviation = models.CharField(
    max_length=5, help_text='Business name abbreviation')
  company_address = models.CharField(max_length=50, help_text='Address of business')
  
  country = CountryField(default='KE')
  annual_sales_revenue = models.IntegerField(choices=REVENUE_RANGE)
  entity = models.CharField(max_length=1, choices=ENTITY_CHOICES)
  accounting_software = models.CharField(max_length=2, choices=ACCOUNTS_SOFTWARE)

  def __str__(self):
    return 'Business {}'.format(self.business_abbreviation)
  
  def aggregate_values_by_type(self, date_range, type, aggregate_over):
    return self.transactions.filter(
      transaction_date__range=date_range, transaction_type=type
      ).aggregate(total=Coalesce(Sum(aggregate_over),0))
  
  def cash_flow(self, date_range):
    total_orders = self.aggregate_values_by_type(
      date_range, 'Order', 'total_transaction_amount')
    
    total_order_payments = self.aggregate_values_by_type(
      date_range, 'Order Payment', 'total_transaction_amount')
    
    total_bills = self.aggregate_values_by_type(
      date_range, 'Bill', 'total_transaction_amount')
    total_bill_payments = self.aggregate_values_by_type(
      date_range, 'Bill Payment', 'total_transaction_amount')
    
    return {
      'amount_in': total_orders['total'] - total_order_payments['total'],
      'bills_due': total_bills['total']- total_bill_payments['total']
    }

  def top_five_items_by_quantity(self, date_range):
    items_ordered_by_quantity =  self.transactions.filter(
      transaction_type='Order', transaction_date__range=date_range
      ).values('item', 'transaction_type').annotate(
      total=Sum('quantity')).order_by('-total')

    items_billed_by_quantity =  self.transactions.filter(
      transaction_type='Bill', transaction_date__range=date_range
      ).values('item', 'transaction_type').annotate(
      total=Sum('quantity')).order_by('-total')
    return {
      'items_ordered_by_quantity': items_ordered_by_quantity[:5],
      'items_billed_by_quantity': items_billed_by_quantity[:5],
    }

  def top_five_items_by_value(self, date_range):
    items_ordered_by_value =  self.transactions.filter(
      transaction_type='Order', transaction_date__range=date_range
      ).values('item', 'transaction_type').annotate(
      total=Sum('total_transaction_amount')).order_by('-total')

    items_billed_by_value =  self.transactions.filter(
      transaction_type='Bill', transaction_date__range=date_range
      ).values('item', 'transaction_type').annotate(
      total=Sum('total_transaction_amount')).order_by('-total')
    return {
      'items_ordered_by_value': items_ordered_by_value[:5],
      'items_billed_by_value': items_billed_by_value[:5],
    }

