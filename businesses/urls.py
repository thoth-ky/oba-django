from django.urls import path

from businesses.views import BusinessList, BusinessDetails


urlpatterns = [
  path('', BusinessList.as_view(), name='business'),
  path('login', BusinessDetails.as_view(), name='business_details'),
]
