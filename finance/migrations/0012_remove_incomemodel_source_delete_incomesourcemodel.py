# Generated by Django 5.0 on 2024-02-25 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0011_expensecategorymodel_expensemodel_expensetypemodel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomemodel',
            name='source',
        ),
        migrations.DeleteModel(
            name='IncomeSourceModel',
        ),
    ]