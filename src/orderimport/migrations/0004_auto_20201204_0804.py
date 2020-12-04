# Generated by Django 3.0.5 on 2020-12-04 01:04

from django.db import migrations, models
import orderimport.models


class Migration(migrations.Migration):

    dependencies = [
        ('orderimport', '0003_order_seperate_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='do',
            field=models.ImageField(blank=True, null=True, upload_to=orderimport.models.image_file_name, verbose_name='Delivery Document'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref',
            field=models.CharField(max_length=20),
        ),
    ]
