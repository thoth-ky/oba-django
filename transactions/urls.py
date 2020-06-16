from django.urls import path

from transactions.views import FileUploadView


urlpatterns = [
  path('business/<int:business_id>/csv_upload', FileUploadView.as_view(), name='file_upload'),
]
