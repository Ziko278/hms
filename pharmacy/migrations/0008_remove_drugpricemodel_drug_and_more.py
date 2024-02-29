# Generated by Django 5.0 on 2024-02-27 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0007_drugpricemodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drugpricemodel',
            name='drug',
        ),
        migrations.RemoveField(
            model_name='drugmodel',
            name='quantity_available',
        ),
        migrations.RemoveField(
            model_name='drugmodel',
            name='selling_price',
        ),
        migrations.RemoveField(
            model_name='drugstockmodel',
            name='drug',
        ),
        migrations.RemoveField(
            model_name='drugstockmodel',
            name='strength',
        ),
        migrations.RemoveField(
            model_name='drugstockmodel',
            name='unit',
        ),
        migrations.CreateModel(
            name='DrugVariantModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.CharField(choices=[('capsule', 'CAPSULE'), ('injection', 'INJECTION'), ('syrup', 'SYRUP'), ('balm', 'BALM')], default='capsule', max_length=50)),
                ('quantity', models.FloatField(blank=True, default=0)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.drugmodel')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pharmacy.drugmanufacturermodel')),
                ('strength', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.drugstrengthmodel')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.drugunitmodel')),
            ],
        ),
        migrations.AddField(
            model_name='drugstockmodel',
            name='drug_variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pharmacy.drugvariantmodel'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='DrugVariantPriceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance', models.CharField(blank=True, choices=[('nhis', 'NHIS')], max_length=100, null=True)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('drug_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_prices', to='pharmacy.drugvariantmodel')),
            ],
        ),
        migrations.DeleteModel(
            name='DrugAvailabilityModel',
        ),
        migrations.DeleteModel(
            name='DrugPriceModel',
        ),
    ]
