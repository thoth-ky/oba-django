from django.urls import path

from transactions.views import FileUploadView, TransactionsList


urlpatterns = [
  path('business/<int:business_id>/csv_upload', FileUploadView.as_view(), name='file_upload'),
  path('business/<int:business_id>/transactions', TransactionsList.as_view(), name='business_transactions'),
]
