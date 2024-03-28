# Generated by Django 5.0 on 2024-03-28 09:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medication', '0001_initial'),
        ('patient', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TestFieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('field_code', models.CharField(max_length=50)),
                ('result_type', models.CharField(choices=[('value', 'VALUE'), ('observation', 'OBSERVATION')], default='value', max_length=50)),
                ('normal_lower_limit', models.FloatField(blank=True, null=True)),
                ('normal_upper_limit', models.FloatField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestObservationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('positive', 'POSITIVE'), ('normal', 'NORMAL'), ('negative', 'NEGATIVE')], default='normal', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestPriceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance', models.CharField(blank=True, choices=[('nhis', 'NHIS')], max_length=100, null=True)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestUnitModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConductTestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('payment_made', models.BooleanField(blank=True, default=False)),
                ('sample_collected', models.BooleanField(blank=True, default=False)),
                ('sample_label', models.CharField(blank=True, max_length=100, null=True)),
                ('conducted', models.CharField(blank=True, choices=[('internal', 'INTERNAL'), ('external', 'EXTERNAL')], max_length=20, null=True)),
                ('result_ready', models.BooleanField(blank=True, default=False)),
                ('admission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medication.admissionmodel')),
                ('collection_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_sample_user', to=settings.AUTH_USER_MODEL)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.patientmodel')),
                ('payment_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_payment_user', to=settings.AUTH_USER_MODEL)),
                ('result_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_result_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConductTestResultModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_result', models.JSONField(blank=True, null=True)),
                ('lab_attendant_comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('type', models.CharField(blank=True, default='test_result', max_length=20)),
                ('admission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medication.admissionmodel')),
                ('attendant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('test', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='laboratory.conducttestmodel')),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('fields', models.ManyToManyField(blank=True, to='laboratory.testfieldmodel')),
                ('possible_sicknesses', models.ManyToManyField(blank=True, to='medication.sicknessmodel')),
            ],
        ),
        migrations.AddField(
            model_name='conducttestmodel',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratory.testmodel'),
        ),
        migrations.AddConstraint(
            model_name='testobservationmodel',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_test_observation_name_combo'),
        ),
        migrations.AddField(
            model_name='testpricemodel',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='laboratory.testmodel'),
        ),
        migrations.AddConstraint(
            model_name='testunitmodel',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_test_unit_name_combo'),
        ),
        migrations.AddField(
            model_name='testfieldmodel',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='laboratory.testunitmodel'),
        ),
        migrations.AddConstraint(
            model_name='testmodel',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_test_name_combo'),
        ),
        migrations.AddConstraint(
            model_name='testfieldmodel',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_test_field_name_combo'),
        ),
    ]
