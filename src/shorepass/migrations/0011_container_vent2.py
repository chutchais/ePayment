# Generated by Django 3.0.5 on 2020-12-01 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorepass', '0010_container_vent'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='vent2',
            field=models.CharField(blank=True, default='', max_length=5, null=True),
        ),
    ]
