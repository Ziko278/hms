from datetime import datetime

from django.db import models
from django.contrib.auth.models import User, Group
from admin_site.models import GeneralSettingModel
from admin_site.model_info import *
from user_management.models import UserProfileModel
# import barcode
from django.apps import apps
from medication.models import SicknessModel, AdmissionModel
from patient.models import PatientModel


class TestUnitModel(models.Model):
    """"""
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_test_unit_name_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()


class TestObservationModel(models.Model):
    """"""
    name = models.CharField(max_length=100)
    STATUS = (('positive', 'POSITIVE'), ('normal', 'NORMAL'), ('negative', 'NEGATIVE'))
    status = models.CharField(max_length=20, choices=STATUS, default='normal')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_test_observation_name_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()


class TestFieldModel(models.Model):
    """"""
    name = models.CharField(max_length=200)
    field_code = models.CharField(max_length=50)
    RESULT_TYPE = (('value', 'VALUE'), ('observation', 'OBSERVATION'))
    result_type = models.CharField(max_length=50, default='value', choices=RESULT_TYPE)
    unit = models.ForeignKey(TestUnitModel, on_delete=models.SET_NULL, null=True, blank=True)
    normal_lower_limit = models.FloatField(blank=True, null=True)
    normal_upper_limit = models.FloatField(blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_test_field_name_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def range(self):
        if self.result_type == 'value':
            return "{} - {} {}".format(self.normal_lower_limit, self.normal_upper_limit, self.unit if self.unit else '')
        return ""


class TestModel(models.Model):
    """"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200, null=True, blank=True)
    fields = models.ManyToManyField(TestFieldModel, blank=True)
    possible_sicknesses = models.ManyToManyField(SicknessModel, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ACTIVE_STATUS, blank=True, default='active')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_test_name_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()


class TestPriceModel(models.Model):
    """"""
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE, related_name='prices')
    insurance = models.CharField(max_length=100, blank=True, null=True, choices=INSURANCE_PROVIDER)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class ConductTestModel(models.Model):
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    cost = models.FloatField(null=True, blank=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    payment_made = models.BooleanField(default=False, blank=True)
    payment_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='test_payment_user')
    sample_collected = models.BooleanField(default=False, blank=True)
    sample_label = models.CharField(max_length=100, blank=True, null=True)
    collection_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='test_sample_user')
    conducted = models.CharField(max_length=20, choices=CONDUCTED_STATUS, blank=True, null=True)
    result_ready = models.BooleanField(default=False, blank=True)
    result_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='test_result_user')
    admission = models.ForeignKey(AdmissionModel, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.test.__str__()

    def result_computed(self):
        test_result = ConductTestResultModel.objects.filter(test=self)
        if len(test_result) > 0:
            return True
        return False

    def save(self, *args, **kwargs):
        today = datetime.today()
        if self.patient.last_visit.year != today.year and self.patient.last_visit.month != today.month and self.patient.last_visit.day != today.day:
            self.patient.number_of_visits += 1
            self.patient.last_visit = today
            self.patient.save()

        super(ConductTestModel, self).save(*args, **kwargs)


class ConductTestResultModel(models.Model):
    test = models.OneToOneField(ConductTestModel, on_delete=models.CASCADE)
    test_result = models.JSONField(blank=True, null=True)
    lab_attendant_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    attendant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, default='test_result', blank=True)
    admission = models.ForeignKey(AdmissionModel, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.test.__str__()

    def save(self, *args, **kwargs):
        if self.test.admission:
            self.admission = self.test.admission

        super(ConductTestResultModel, self).save(*args, **kwargs)