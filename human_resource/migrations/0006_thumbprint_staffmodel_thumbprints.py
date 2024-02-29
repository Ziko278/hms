# Generated by Django 5.0 on 2024-02-02 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0005_alter_staffmodel_bank_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThumbPrint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbprint_data', models.BinaryField()),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human_resource.staffmodel')),
            ],
        ),
        migrations.AddField(
            model_name='staffmodel',
            name='thumbprints',
            field=models.ManyToManyField(blank=True, to='human_resource.thumbprint'),
        ),
    ]