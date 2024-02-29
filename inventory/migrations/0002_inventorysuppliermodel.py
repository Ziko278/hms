# Generated by Django 5.0 on 2024-01-27 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventorySupplierModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('phone_number', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField()),
                ('contact_name', models.CharField(blank=True, max_length=250, null=True)),
                ('contact_phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]