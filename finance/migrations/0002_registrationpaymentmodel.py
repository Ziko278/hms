# Generated by Django 5.0 on 2024-01-17 23:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationPaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('registration_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.patientregistrationfeemodel')),
            ],
        ),
    ]