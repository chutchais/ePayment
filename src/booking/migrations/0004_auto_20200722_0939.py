# Generated by Django 3.0.7 on 2020-07-22 02:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20200623_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Name does not allow special charecters', regex='^[\\w-]+$')], verbose_name='Booking number'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='terminal',
            field=models.CharField(blank=True, choices=[('LCB1', 'LCB1'), ('LCMT', 'LCMT')], max_length=10, null=True),
        ),
    ]
