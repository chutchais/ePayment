# Generated by Django 3.0.7 on 2020-06-24 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oog', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='oog',
            index=models.Index(fields=['booking', 'container'], name='idx_oog_oog_booking_container'),
        ),
        migrations.AddIndex(
            model_name='oog',
            index=models.Index(fields=['container'], name='idx_oog_oog_container'),
        ),
    ]
