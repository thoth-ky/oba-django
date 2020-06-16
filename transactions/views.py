from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from businesses.models import Business

from transactions.serializers import FileSerializer, TransactionSerializer

class FileUploadView(generics.GenericAPIView):
  serializer_class = FileSerializer
  parser_classes = (MultiPartParser,)

  def get_permissions(self):
    business = get_object_or_404(Business, id=self.kwargs.get('business_id'))
    if business not in  self.request.user.businesses.all():
      raise PermissionDenied
    else:
      self.permission_classes = [IsAuthenticated,]
    return super(FileUploadView, self).get_permissions()

  def post(self, *args, **kwargs):
    context = {
      'request': self.request,
      'business_id': self.kwargs.get('business_id')
    }
    serializer = FileSerializer(data=self.request.data, context=context)
    
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
      'message': 'CSV uploaded and saved into database successfully'
    }, status=HTTP_201_CREATED)

class TransactionsList(generics.ListAPIView):
  serializer_class = TransactionSerializer
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    business = get_object_or_404(Business, id=self.kwargs.get('business_id'))
    return business.transactions.all()
