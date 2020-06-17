from django.urls import path
from datetime import datetime, timedelta

from businesses.views import BusinessList, BusinessDetails, BusinessTransactions

date_format = '%Y-%m-%d'
end = datetime.strftime(datetime.now(), date_format)
start = datetime.strftime(datetime.now() - timedelta(30), date_format)

urlpatterns = [
  path('', BusinessList.as_view(), name='business'),
  path('<int:pk>', BusinessDetails.as_view(), name='business_details'),
  path('<int:pk>/dashboard', BusinessTransactions.as_view(), kwargs={'from': start, 'to': end }, name='business_transactions'),  
]
