# Generated by Django 5.0 on 2024-02-21 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_inventorystockoutmodel_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorystockmodel',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='inventorystockmodel',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='inventorystockmodel',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]