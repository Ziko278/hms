from django.db import models
from django.contrib.auth.models import User, Group
from admin_site.model_info import *
from admin_site.models import GeneralSettingModel
import random
# import barcode
from datetime import date
# from barcode.writer import ImageWriter
from django.apps import apps
from finance.models import RegistrationPaymentModel
from admin_site.models import GeneralSettingModel


# def generate_barcode(identifier):
#     code = barcode.Code39(identifier, writer=ImageWriter(), add_checksum=False)
#     file_name = f'{identifier}'
#     file_path = f'media/barcode/student/{file_name}'
#     code.save(file_path)
#     #
#     return file_path + '.png'


class PatientModel(models.Model):
    """"""

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    address = models.CharField(max_length=250, null=True, blank=True)

    image = models.FileField(blank=True, null=True, upload_to='images/patient')
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS, null=True, blank=True)
    religion = models.CharField(max_length=30, choices=RELIGION, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)

    blood_group = models.CharField(max_length=20, choices=BLOOD_GROUP, null=True, blank=True)
    genotype = models.CharField(max_length=20, choices=GENOTYPE, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    medical_conditions = models.TextField(null=True, blank=True)

    emergency_contact_name = models.CharField(max_length=200,  null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20,  null=True, blank=True)

    insurance_provider = models.CharField(max_length=100, choices=INSURANCE_PROVIDER, null=True, blank=True)
    insurance_provider_number = models.CharField(max_length=100, null=True, blank=True)

    registration_date = models.DateField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, default='active')
    # barcode = models.FileField(upload_to='barcode/patient', null=True, blank=True)
    registration_payment = models.ForeignKey(RegistrationPaymentModel, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_created_by')
    number_of_visits = models.IntegerField(blank=True, default=1)
    last_visit = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        if self.middle_name:
            return "{} {} {}".format(self.first_name, self.middle_name,  self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)

    def consultation_fee(self):
        ConsultationFeeModel = apps.get_model('consultation', 'ConsultationFeeModel')
        consultation = ConsultationFeeModel.objects.filter(insurance=self.insurance_provider).first()
        if not consultation:
            consultation = ConsultationFeeModel.objects.filter(insurance=None).first()
        if not consultation:
            consultation = ConsultationFeeModel.objects.first()
        if not consultation:
            consultation_fee = 0
        else:
            consultation = consultation.amount
        return consultation

    def today_vital(self):
        vital = PatientVitalsModel.objects.filter(patient=self, date=date.today()).first()
        if vital:
            return vital
        return False

    def save(self, *args, **kwargs):
        if not self.last_visit:
            self.last_visit = date.today()
        patient_setting = GeneralSettingModel.objects.first()

        if patient_setting.auto_generate_card_number and not self.card_number:
            last_patient = PatientIDGeneratorModel.objects.filter(status='s').last()
            if last_patient:
                patient_id = str(int(last_patient.last_id) + 1)
            else:
                patient_id = str(1)
            while True:
                gen_id = patient_id
                patient_id = 'pat-' + patient_id.rjust(4, '0')
                patient_exist = PatientModel.objects.filter(card_number=patient_id).first()
                if not patient_exist:
                    break
                else:
                    patient_id = str(int(gen_id) + 1)
            self.card_number = patient_id

            generate_id = PatientIDGeneratorModel.objects.create(last_id=gen_id, last_patient_id=self.card_number, status='f')
            generate_id.save()

        super(PatientModel, self).save(*args, **kwargs)

    def admission_price(self):
        AdmissionFeeModel = apps.get_model('finance', 'AdmissionFeeModel')
        admission = None
        if self.insurance_provider:
            admission = AdmissionFeeModel.objects.filter(insurance=self.insurance_provider).first()
        if not admission:
            admission = AdmissionFeeModel.objects.filter(insurance=None).first()
        if not admission:
            admission = AdmissionFeeModel.objects.first()
        if admission:
            price = admission.amount
        else:
            price = 0
        return price
    
    def delivery_price(self):
        DeliveryFeeModel = apps.get_model('finance', 'DeliveryFeeModel')
        delivery = None
        if self.insurance_provider:
            delivery = DeliveryFeeModel.objects.filter(insurance=self.insurance_provider).first()
        if not delivery:
            delivery = DeliveryFeeModel.objects.filter(insurance=None).first()
        if not delivery:
            delivery = DeliveryFeeModel.objects.first()
        if delivery:
            price = delivery.amount
        else:
            price = 0
        return price


class PatientVitalsModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    bp_diastolic = models.IntegerField()
    bp_systolic = models.IntegerField()
    pulse = models.IntegerField(blank=True, null=True)
    temperature = models.IntegerField(blank=True, null=True)
    respiratory_rate = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    extra_note = models.TextField(null=True, blank=True)
    date = models.DateField(blank=True, auto_now_add=True)


class PatientIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_patient_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS = (
        ('s', 'SUCCESS'), ('f', 'FAIL')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, default='f')


class PatientProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='user_patient_profile')
    patient = models.OneToOneField(PatientModel, on_delete=models.CASCADE, null=True, related_name='patient_profile')
    default_password = models.CharField(max_length=20)

    def __str__(self):
        return self.patient.__str__()


class PatientMonthlyStatisticModel(models.Model):
    date = models.DateField(auto_now_add=True)
    no_of_new_patient = models.IntegerField(default=1)
    no_of_returning_patient = models.IntegerField(default=1)
    patients = models.ManyToManyField(PatientModel)

