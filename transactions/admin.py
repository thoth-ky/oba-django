from django.contrib import admin
from transactions.models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
  list_display = ('transaction_id','business', 'transaction_type', 'transaction_status', 'transaction_date')

admin.site.register(Transaction, TransactionAdmin)