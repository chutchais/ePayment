# Generated by Django 3.0.5 on 2020-10-28 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0007_order_seperate_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='execute_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='execute_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='wht_slip',
            field=models.ImageField(blank=True, null=True, upload_to=order.models.image_file_name),
        ),
    ]
