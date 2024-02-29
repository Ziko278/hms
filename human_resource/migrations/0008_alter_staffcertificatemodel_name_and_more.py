# Generated by Django 5.0 on 2024-02-03 07:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0007_staffprofilemodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffcertificatemodel',
            name='name',
            field=models.CharField(default='ll', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staffprofilemodel',
            name='staff',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff_profile', to='human_resource.staffmodel'),
        ),
        migrations.AlterField(
            model_name='staffprofilemodel',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_staff_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
