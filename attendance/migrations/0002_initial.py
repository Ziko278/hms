# Generated by Django 5.0 on 2024-03-28 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendance', '0001_initial'),
        ('human_resource', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffattendancemodel',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human_resource.staffmodel'),
        ),
    ]
