# Generated by Django 3.0.7 on 2020-06-16 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20200616_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('Order', 'Order'), ('Order payment', 'Order payment'), ('Bill', 'Bill'), ('Bill Payment', 'Bill Payment)')], max_length=15),
        ),
    ]