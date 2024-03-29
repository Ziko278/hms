# Generated by Django 5.0 on 2024-03-28 09:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communication', '0001_initial'),
        ('human_resource', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmodel',
            name='sender',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_sender', to='human_resource.staffmodel'),
        ),
        migrations.AddField(
            model_name='emailmodel',
            name='staff',
            field=models.ManyToManyField(blank=True, to='human_resource.staffmodel'),
        ),
        migrations.AddField(
            model_name='messagemodel',
            name='receiver',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='human_resource.staffmodel'),
        ),
        migrations.AddField(
            model_name='messagemodel',
            name='sender',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='human_resource.staffmodel'),
        ),
        migrations.AddField(
            model_name='notemodel',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recentactivitymodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='smtpconfigurationmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='communicationsettingmodel',
            name='default_smtp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='communication.smtpconfigurationmodel'),
        ),
    ]
