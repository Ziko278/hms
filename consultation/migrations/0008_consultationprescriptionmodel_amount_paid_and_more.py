# Generated by Django 5.0 on 2024-01-27 05:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0007_rename_consultation_consultationmodel_detail_and_more'),
        ('medication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationprescriptionmodel',
            name='amount_paid',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultationprescriptionmodel',
            name='grand_total',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultationprescriptionmodel',
            name='sale_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultationtestmodel',
            name='amount_paid',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultationtestmodel',
            name='grand_total',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prescriptionmodel',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prescriptionmodel',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='prescriptionmodel',
            name='pres_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prescriptionmodel',
            name='quantity',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prescriptionmodel',
            name='total_price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prescriptionmodel',
            name='unit_cost_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prescriptionmodel',
            name='unit_selling_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='consultationprescriptionmodel',
            name='prescription',
            field=models.ManyToManyField(to='consultation.prescriptionmodel'),
        ),
        migrations.CreateModel(
            name='ConductTestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_id', models.IntegerField()),
                ('cost', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medication.drugmodel')),
            ],
        ),
        migrations.AlterField(
            model_name='consultationtestmodel',
            name='test',
            field=models.ManyToManyField(to='consultation.conducttestmodel'),
        ),
    ]
