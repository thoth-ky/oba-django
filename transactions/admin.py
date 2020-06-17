from django.contrib import admin
from transactions.models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
  list_display = ('transaction_id','business', 'item', 'transaction_type', 'transaction_status', 'transaction_date', 'quantity', 'total_transaction_amount')
  list_filter = ('business','transaction_status', 'transaction_type', 'item', 'transaction_date')

admin.site.register(Transaction, TransactionAdmin)