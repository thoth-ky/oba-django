from django.db import models
from businesses.models import Business


TRANSACTIONS =(
  ('Order','Order'),
  ('Order payment','Order payment'),
  ('Bill','Bill'),
  ('Bill Payment','Bill Payment)'),
)
STATUSES = (
  ('Pending', 'Pending'),
  ('Accepted', 'Accepted'),
  ('Rejected', 'Rejected'),
  ('Completed', 'Completed'),
  ('Open', 'Open'),
  ('Closed', 'Closed'),
)


class Transaction(models.Model):
  business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='transactions')

  transaction_type = models.CharField(max_length=15, choices=TRANSACTIONS)
  transaction_id = models.IntegerField()
  transaction_status = models.CharField(max_length=10, choices=STATUSES)
  transaction_date = models.DateField()
  due_date= models.DateField(blank=True, null=True)
  customer_or_supplier = models.CharField(max_length=50)
  item = models.CharField(max_length=50)
  quantity = models.IntegerField()
  unit_amount = models.FloatField()
  total_transaction_amount = models.FloatField()

  def __str__(self):
    return f'Transaction {self.transaction_id} ID: {self.id}'
