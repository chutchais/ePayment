# Generated by Django 3.0.5 on 2020-08-17 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_qrid'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['qrid'], name='idx_order_qrid'),
        ),
    ]
