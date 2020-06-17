from django.db import models
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
  owner = models.ForeignKey(User, related_name='businesses', on_delete=models.PROTECT)
  name = models.CharField(max_length=25, help_text='Name of business')
  business_abbreviation = models.CharField(max_length=5, help_text='Business name abbreviation')
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
      ).aggregate(models.Sum(aggregate_over))

