# Generated by Django 5.0 on 2024-02-27 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_inventoryitemmodel_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorystockoutmodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
