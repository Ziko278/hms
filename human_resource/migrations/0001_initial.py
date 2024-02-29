# Generated by Django 5.0 on 2024-01-14 12:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HRSettingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_generate_staff_id', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PositionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaffCertificateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('certificate', models.FileField(upload_to='document/staff/certificate')),
                ('date_obtained', models.DateField(blank=True, null=True)),
                ('certificate_type', models.CharField(blank=True, choices=[('school leaving', 'SCHOOL LEAVING'), ('ond', 'OND'), ('hnd', 'HND')], max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaffIDGeneratorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_id', models.IntegerField()),
                ('last_staff_id', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('s', 'SUCCESS'), ('f', 'FAIL')], default='f', max_length=10)),
                ('type', models.CharField(blank=True, choices=[('pri', 'PRIMARY'), ('sec', 'SECONDARY')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StaffModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('image', models.FileField(blank=True, null=True, upload_to='images/staff')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE')], max_length=10)),
                ('marital_status', models.CharField(blank=True, choices=[('single', 'SINGLE'), ('married', 'MARRIED'), ('widowed', 'WIDOWED'), ('divorced', 'DIVORCED')], max_length=30, null=True)),
                ('religion', models.CharField(blank=True, choices=[('christianity', 'CHRISTIANITY'), ('islam', 'ISLAM'), ('others', 'OTHERS')], max_length=30, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('lga', models.CharField(blank=True, max_length=100, null=True)),
                ('staff_id', models.CharField(blank=True, max_length=100, null=True)),
                ('employment_date', models.DateField(blank=True, null=True)),
                ('cv', models.FileField(blank=True, null=True, upload_to='staff/cv')),
                ('salary', models.BigIntegerField(blank=True, default=0, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'), ('o-', 'O-')], max_length=20, null=True)),
                ('genotype', models.CharField(blank=True, choices=[('aa', 'AA'), ('as', 'AS'), ('ac', 'AC'), ('ss', 'SS')], max_length=20, null=True)),
                ('medical_conditions', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default='active', max_length=30)),
                ('barcode', models.FileField(blank=True, null=True, upload_to='barcode/staff')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='departmentmodel',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_dept_name_combo'),
        ),
        migrations.AddField(
            model_name='positionmodel',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='human_resource.departmentmodel'),
        ),
        migrations.AddField(
            model_name='staffmodel',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_staffs', to='human_resource.departmentmodel'),
        ),
        migrations.AddField(
            model_name='staffmodel',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
        migrations.AddField(
            model_name='staffmodel',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_staffs', to='human_resource.positionmodel'),
        ),
        migrations.AddField(
            model_name='staffmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='staffcertificatemodel',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human_resource.staffmodel'),
        ),
        migrations.AddConstraint(
            model_name='positionmodel',
            constraint=models.UniqueConstraint(fields=('name', 'department'), name='unique_dept_name_and_dept_combo'),
        ),
        migrations.AddConstraint(
            model_name='staffmodel',
            constraint=models.UniqueConstraint(fields=('staff_id',), name='unique_staff_id'),
        ),
    ]
