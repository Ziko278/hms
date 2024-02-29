# Generated by Django 5.0 on 2024-01-14 12:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientIDGeneratorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_id', models.IntegerField()),
                ('last_student_id', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('s', 'SUCCESS'), ('f', 'FAIL')], default='f', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PatientSettingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_generate_card_number', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('card_number', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE')], max_length=10)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='images/patient')),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('single', 'SINGLE'), ('married', 'MARRIED'), ('widowed', 'WIDOWED'), ('divorced', 'DIVORCED')], max_length=30, null=True)),
                ('religion', models.CharField(blank=True, choices=[('christianity', 'CHRISTIANITY'), ('islam', 'ISLAM'), ('others', 'OTHERS')], max_length=30, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('lga', models.CharField(blank=True, max_length=100, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'), ('o-', 'O-')], max_length=20, null=True)),
                ('genotype', models.CharField(blank=True, choices=[('aa', 'AA'), ('as', 'AS'), ('ac', 'AC'), ('ss', 'SS')], max_length=20, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('medical_conditions', models.TextField(blank=True, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=200, null=True)),
                ('emergency_contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('insurance_provider', models.CharField(blank=True, choices=[('nhis', 'NHIS'), ('others', 'OTHERS')], max_length=100, null=True)),
                ('insurance_provider_number', models.CharField(blank=True, max_length=100, null=True)),
                ('registration_date', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(blank=True, default='active', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medication', models.ManyToManyField(blank=True, to='medication.drugmodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]