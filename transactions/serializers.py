import csv, io
from datetime import datetime
from django.core.exceptions import ValidationError
from rest_framework import serializers



from businesses.serializers import BusinessSerializer
from businesses.models import Business

from transactions.validators import (
  validate_file_extension,
  validate_required_fields,
  validate_dates,  
  CSV_HEADERS)
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
  business = BusinessSerializer(required=False)
  class Meta:
    model = Transaction
    fields = '__all__'
  
  def create(self, validated_data):
    return Transaction.objects.create(business_id=self.context['business_id'], **validated_data)

class FileSerializer(serializers.Serializer):
  csv_file = serializers.FileField(
    help_text='CSV file containing transaction details',
    validators=[validate_file_extension,]
    )
  
  def validate(self, data):
    transactions = csv.reader(io.StringIO(data['csv_file'].read().decode('utf-8')))
    headers = next(transactions)
    if headers != CSV_HEADERS:
      raise ValidationError(f'Headers do not match expected. Order matters {CSV_HEADERS}')
    
    csv_data = []
    # business_id = self.context['business_id']
    DATE_INPUT_FORMAT = '%m/%d/%Y'

    def convert_date(cell):
      if cell in (None, ""):
        return ""
      return datetime.strptime(cell, DATE_INPUT_FORMAT).strftime('%Y-%m-%d')
    
    for row in transactions:
      validate_required_fields(row)
      validate_dates(row)
      csv_data.append({
          'transaction_type': row[0],
          'transaction_id': row[1],
          'transaction_status': row[2],
          'transaction_date': convert_date(row[3]),
          'due_date': convert_date(row[4]),
          'customer_or_supplier': row[5],
          'item': row[6],
          'quantity': row[7],
          'unit_amount': row[8],
          'total_transaction_amount': row[9],
        })
    validated_data = {'csv_data': csv_data}
    return validated_data
  
  def create(self, validated_data):
    trans_serializer = TransactionSerializer(data=validated_data['csv_data'], many=True, context=self.context)
    trans_serializer.is_valid(raise_exception=True)
    return trans_serializer.save()
    
    