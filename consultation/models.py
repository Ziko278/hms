from datetime import datetime

from django.db import models
from django.contrib.auth.models import User, Group
from admin_site.models import GeneralSettingModel
from admin_site.model_info import *
from medication.models import AdmissionModel
from pharmacy.models import DrugModel, DrugVariantModel
from user_management.models import UserProfileModel
from patient.models import PatientModel, PatientMonthlyStatisticModel
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cons_payment_user')

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

        today = datetime.today()
        if self.patient.last_visit != today:
            self.patient.number_of_visits += 1
        self.patient.last_visit = today
        self.patient.save()

        current_date = datetime.today()
        stat = PatientMonthlyStatisticModel.objects.filter(date__year=current_date.year,
                                                           date__month=current_date.month).first()
        if stat:
            if self.patient not in stat.patients.all():
                stat.no_of_returning_patient += 1
                stat.save()
                stat.patients.add(self.patient)
        else:
            stat = PatientMonthlyStatisticModel.objects.create()
            stat.save()
            if stat.id:
                stat.patients.add(self.patient)

        old_stat_list = PatientMonthlyStatisticModel.objects.exclude(date__year=current_date.year,
                                                                     date__month=current_date.month)
        for stat in old_stat_list:
            stat.patients = None
            stat.save()

        super(ConsultationPaymentModel, self).save(*args, **kwargs)


class DoctorConsultationQueueModel(models.Model):
    doctor = models.OneToOneField(StaffModel, on_delete=models.CASCADE, related_name='doctor_queue')
    block = models.ForeignKey(ConsultationBlockModel, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(ConsultationRoomModel, on_delete=models.SET_NULL, null=True, blank=True)
    patients = models.ManyToManyField(PatientModel, blank=True)
    doctor_status = models.CharField(max_length=30, choices=ACTIVE_STATUS, default='active')
    posting_status = models.CharField(max_length=30, choices=ACTIVE_STATUS, default='active')

    def __str__(self):
        return self.doctor.__str__()


class ConsultationModel(models.Model):
    doctor = models.ForeignKey(StaffModel, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    status = models.CharField(max_length=30, choices=CONSULTATION_STAGE, default='new')
    admission = models.ForeignKey(AdmissionModel, null=True, on_delete=models.SET_NULL, blank=True)
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=30, blank=True, default='consultation')

    def __str__(self):
        return "{} - {}".format(self.patient.__str__(), self.created_at)


class PrescriptionModel(models.Model):
    drug = models.ForeignKey(DrugVariantModel, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.FloatField()
    unit_selling_price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    drug_available = models.BooleanField(default=False, blank=True)
    payment_made = models.BooleanField(default=False, blank=True)
    payment_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pres_payment_user')
    collected = models.BooleanField(default=False, blank=True)
    collection_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='pres_collect_user')
    admission = models.ForeignKey(AdmissionModel, null=True, on_delete=models.SET_NULL, blank=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.SET_NULL, null=True, related_name='prescription_patient')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='prescription_doctor')

    def __str__(self):
        return self.drug.__str__()

    def save(self, *args, **kwargs):
        if float(self.drug.quantity) >= float(self.quantity):
            self.drug_available = True

        super(PrescriptionModel, self).save(*args, **kwargs)


class ConsultationPrescriptionModel(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.SET_NULL, null=True)
    prescriptions = models.ManyToManyField(PrescriptionModel)
    grand_total = models.FloatField(blank=True, default=0)
    amount_paid = models.FloatField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    type = models.CharField(max_length=30, blank=True, default='prescription')
    admission = models.ForeignKey(AdmissionModel, null=True, on_delete=models.SET_NULL, blank=True)

    def save(self, *args, **kwargs):
        today = datetime.today()

        if self.patient.last_visit.year != today.year or self.patient.last_visit.month != today.month or self.patient.last_visit.day != today.day:
            self.patient.number_of_visits += 1
            self.patient.last_visit = today
            self.patient.save()

        super(ConsultationPrescriptionModel, self).save(*args, **kwargs)


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
    admission = models.ForeignKey(AdmissionModel, null=True, on_delete=models.SET_NULL, blank=True)

    def save(self, *args, **kwargs):
        today = datetime.today()

        if self.patient.last_visit.year != today.year and self.patient.last_visit.month != today.month and self.patient.last_visit.day != today.day:
            self.patient.number_of_visits += 1
            self.patient.last_visit = today
            self.patient.save()

        super(ConsultationTestModel, self).save(*args, **kwargs)



