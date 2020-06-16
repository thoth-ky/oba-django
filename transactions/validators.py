import os, csv, io
from datetime import datetime
from django.core.exceptions import ValidationError

CSV_HEADERS = [
  'Transaction',
  'ID',
  'Status',
  'Transaction Date',
  'Due Date',
  'Customer or Supplier',
  'Item',
  'Quantity',
  'Unit Amount',
  'Total Transaction Amount',
  ]

def validate_file_extension(value):
  ext = os.path.splitext(value.name)[1]
  if ext.lower() != '.csv':
    msg = f'Unsupported file extension: {ext}. Only CSV files supported'
    raise ValidationError(msg)

def validate_dates(row):
  
  try:
    datetime.strptime(row[3], '%m/%d/%Y')
    if row[4] not in (None, ""):
      datetime.strptime(row[4], '%m/%d/%Y')
  except:
    raise ValidationError('Ensure all dates are in the format "MM/DD/YYYY"')


def validate_required_fields(row):
  if (row[0] or row[1] or row[3] or row[5] or row[6] or row[7] or row[8] or row[9]) in (None, ""):
    raise ValidationError("Some rows are missing required fields")

  if (row[0] in ("Bill", "Order")) and (row[2] in (None, "")):
    raise ValidationError("Bill or Order transactions require a status")
