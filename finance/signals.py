from datetime import date

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from finance.models import ExpenseModel, IncomeModel
from django.contrib.auth.models import User
from communication.models import RecentActivityModel


@receiver(post_save, sender=ExpenseModel)
def expense_save(sender, instance, created, **kwargs):
    expense = instance
    if created:
        category = 'expense_registration'
        subject = "N{} expense recorded for {}".format(expense.amount, expense.expense_type.__str__())
        recent_activity = RecentActivityModel.objects.create(category=category, subject=subject, reference_id=expense.id,
                                                             user=expense.user)
        recent_activity.save()


@receiver(post_save, sender=IncomeModel)
def income_save(sender, instance, created, **kwargs):
    income = instance
    if created:
        category = 'income_registration'
        subject = "N{} income recorded from {}".format(income.amount, income.category.__str__())
        recent_activity = RecentActivityModel.objects.create(category=category, subject=subject, reference_id=income.id,
                                                             user=income.user)
        recent_activity.save()