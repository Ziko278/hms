# Generated by Django 5.0 on 2024-02-03 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_alter_patientmodel_medication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientmodel',
            name='insurance_provider',
            field=models.CharField(blank=True, choices=[('nhis', 'NHIS')], max_length=100, null=True),
        ),
    ]
