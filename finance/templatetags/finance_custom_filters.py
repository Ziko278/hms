from django import template
from patient.models import PatientModel
from datetime import date, timedelta
from finance.models import *
from django.db.models import Sum
from laboratory.models import TestPriceModel, TestModel

register = template.Library()


@register.filter
def get_patient_test_price(test, patient_id):
    patient = PatientModel.objects.get(pk=patient_id)
    test_price = TestPriceModel.objects.filter(test=test, insurance=patient.insurance_provider).first()
    if not test_price:
        test_price = TestPriceModel.objects.filter(test=test, insurance=None).first()
    if not test_price:
        test_price = TestPriceModel.objects.filter(test=test).first()
    if not test_price:
        price = 0
    else:
        price = test_price.amount
    return price


