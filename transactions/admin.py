from django.contrib import admin
from transactions.models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
  list_display = ('transaction_id','business', 'item', 'transaction_type', 'transaction_status', 'transaction_date')
  list_filter = ('transaction_status', 'transaction_type', 'item')

admin.site.register(Transaction, TransactionAdmin)