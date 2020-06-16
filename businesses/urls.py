from django.urls import path

from businesses.views import BusinessList, BusinessDetails, BusinessTransactions

urlpatterns = [
  path('', BusinessList.as_view(), name='business'),
  path('<int:pk>', BusinessDetails.as_view(), name='business_details'),
  path('<int:pk>/summary', BusinessTransactions.as_view(), name='business_transactions'),
]
