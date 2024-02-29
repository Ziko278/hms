# Generated by Django 5.0 on 2024-01-15 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('human_resource', '0003_staffmodel_is_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffmodel',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
    ]