from django.db import models
from django.contrib.auth.models import User, Group
from admin_site.models import GeneralSettingModel
from admin_site.model_info import *
from pharmacy.models import DrugModel, DrugUnitModel, DrugStrengthModel
from user_management.models import UserProfileModel
from patient.models import PatientModel
from human_resource.models import StaffModel
from django.apps import apps
from laboratory.models import TestModel, ConductTestModel


class ConsultationBlockModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name.title()


class ConsultationRoomModel(models.Model):
    name = models.CharField(max_length=200)
    block = models.ForeignKey(ConsultationBlockModel, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name.title()


class ConsultationFeeModel(models.Model):
    name = models.CharField(max_length=200)
    amount = models.FloatField()
    duration = models.CharField(max_length=100, choices=CONSULTATION_PAYMENT_DURATION, default='daily')
    insurance = models.CharField(max_length=100, null=True, blank=True, choices=INSURANCE_PROVIDER)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class ConsultationPaymentModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(blank=True)
    amount_paid = models.FloatField()
    balance_credited = models.FloatField(blank=True, default=0)
    attendant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount_forfeited = models.FloatField(default=0)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    is_posted = models.BooleanField(default=False, blank=True)
    is_attended = models.BooleanField(default=False, blank=True)
    doctor = models.ForeignKey(StaffModel, on_delete=models.SET_NULL, blank=True, null=True, related_name='consultation_doctor')
    status = models.CharField(max_length=30, choices=CONSULTATION_STATUS, default='not posted', blank=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            last_payment = ConsultationPaymentModel.objects.last()
            if last_payment:
                payment_id = last_payment.id
            else:
                payment_id = 1
            transaction_id = 'trn/cslt/' + str(payment_id).rjust(6, '0')

            self.transaction_id = transaction_id

        if self.patient.insurance_provider:
            general = ConsultationFeeModel.objects.filter(insurance=None).first()
            if general:
                actual_price = general.amount
                self.amount_forfeited = actual_price - self.amount

        super(ConsultationPaymentModel, self).save(*args, **kwargs)


class DoctorConsultationQueueModel(models.Model):
    doctor = models.OneToOneField(StaffModel, on_delete=models.CASCADE, related_name='doctor_queue')
    patients = models.ManyToManyField(PatientModel, blank=True)
    doctor_status = models.CharField(max_length=30, choices=ACTIVE_STATUS, default='active')
    posting_status = models.CharField(max_length=30, choices=ACTIVE_STATUS, default='active')

    def __str__(self):
        return self.doctor.__str__()


class ConsultationModel(models.Model):
    doctor = models.ForeignKey(StaffModel, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    status = models.CharField(max_length=30, choices=CONSULTATION_STAGE, default='new')
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=30, blank=True, default='consultation')

    def __str__(self):
        return "{} - {}".format(self.patient.__str__(), self.created_at)


class PrescriptionModel(models.Model):
    drug = models.ForeignKey(DrugModel, on_delete=models.CASCADE)
    unit = models.ForeignKey(DrugUnitModel, on_delete=models.SET_NULL, null=True, blank=True)
    strength = models.ForeignKey(DrugStrengthModel, on_delete=models.SET_NULL, null=True, blank=True)
    dosage = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.FloatField()
    unit_selling_price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default=PAYMENT_STATUS[0])
    collection_status = models.CharField(max_length=20, choices=COLLECTION_STATUS, default=COLLECTION_STATUS[0])

    def __str__(self):
        return self.drug.__str__()


class ConsultationPrescriptionModel(models.Model):
    doctor = models.ForeignKey(StaffModel, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.SET_NULL, null=True)
    prescriptions = models.ManyToManyField(PrescriptionModel)
    grand_total = models.FloatField(blank=True, default=0)
    amount_paid = models.FloatField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, default='prescription')


class ConsultationTestModel(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.SET_NULL, null=True)
    tests = models.ManyToManyField(ConductTestModel, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    grand_total = models.FloatField()
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    amount_paid = models.FloatField(blank=True, default=0)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default=PAYMENT_STATUS[0])
    type = models.CharField(max_length=30, blank=True, default='test')






