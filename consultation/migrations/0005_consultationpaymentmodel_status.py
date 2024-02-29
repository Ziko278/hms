# Generated by Django 5.0 on 2024-01-20 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0004_remove_doctorconsultationqueuemodel_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationpaymentmodel',
            name='status',
            field=models.CharField(blank=True, choices=[('not posted', 'NOT POSTED'), ('posted', 'posted'), ('progress', 'PROGRESS'), ('complete', 'COMPLETE')], default='not posted', max_length=30),
        ),
    ]