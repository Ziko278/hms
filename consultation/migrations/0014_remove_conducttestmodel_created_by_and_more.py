# Generated by Django 5.0 on 2024-01-27 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0013_prescriptionmodel_unit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conducttestmodel',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='conducttestmodel',
            name='drug',
        ),
    ]
