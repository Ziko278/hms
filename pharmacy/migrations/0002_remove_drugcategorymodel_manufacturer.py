# Generated by Django 5.0 on 2024-01-27 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drugcategorymodel',
            name='manufacturer',
        ),
    ]