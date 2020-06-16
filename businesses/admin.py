from django.contrib import admin

from businesses.models import Business

class BusinessAdmin(admin.ModelAdmin):
  list_display = ('business_abbreviation', 'name', 'owner', 'entity')
  list_filter = ('entity', 'annual_sales_revenue')

admin.site.register(Business, BusinessAdmin)
