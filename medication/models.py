from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Sum
from django.utils import timezone
from admin_site.model_info import *
from patient.models import PatientModel


class SicknessModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name).title()


class WardModel(models.Model):
    name = models.CharField(max_length=100)
    ward_type = models.CharField(max_length=50, choices=WARD_TYPE)
    last_cleaned_date = models.DateField(blank=True, null=True)
    last_cleaned_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name).title()

    def no_of_free_beds(self):
        bed_list = BedModel.objects.filter(ward=self)
        count = 0
        for bed in bed_list:
            if bed.is_free:
                count += 1
        return count

    def free_beds(self):
        bed_list = BedModel.objects.filter(ward=self)
        bed_dict = {}
        for bed in bed_list:
            if bed.is_free:
                bed_dict[bed.id] = bed
        return bed_dict


class BedModel(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(WardModel, on_delete=models.CASCADE, related_name='ward_beds')
    last_cleaned_date = models.DateField(blank=True, null=True)
    last_cleaned_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def is_free(self):
        admission_count = AdmissionModel.objects.filter(status='active', bed=self).count()
        if admission_count > 0:
            return False
        return True


class AdmissionModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    ward = models.ForeignKey(WardModel, on_delete=models.SET_NULL, null=True, blank=True)
    bed = models.ForeignKey(BedModel, on_delete=models.SET_NULL, null=True, blank=True)
    purpose = models.TextField()
    price_per_day = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateField(blank=True, null=True)
    STATUS = (('active', 'ACTIVE'), ('discharged', 'DISCHARGED'))
    status = models.CharField(max_length=50, choices=STATUS, blank=True, default='active')
    discharge_note = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    discharge_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admission_discharge_user')
    patient_discharge_status = models.CharField(max_length=20, choices=MORTALITY_STATUS, default='alive', blank=True)

    def total_cost(self):
        today = timezone.now().date()
        if self.status == 'active':
            days_admitted = (today - self.date).days + 1
        else:
            days_admitted = (self.discharge_date - self.date).days + 1
        admission_fee = days_admitted * self.patient.admission_price()

        ConductTestModel = apps.get_model('laboratory', 'ConductTestModel')
        test_fee = ConductTestModel.objects.filter(
            Q(admission=self) & (Q(sample_collected=True) | Q(result_ready=True))
        ).aggregate(Sum('cost'))['cost__sum']
        test_fee = test_fee if test_fee else 0
        PrescriptionModel = apps.get_model('consultation', 'PrescriptionModel')
        drug_fee = PrescriptionModel.objects.filter(
            Q(admission=self) & Q(collected=True)
        ).aggregate(Sum('total_price'))['total_price__sum']
        drug_fee = drug_fee if drug_fee else 0

        return admission_fee + drug_fee + test_fee

    def amount_paid(self):
        payment = AdmissionPaymentModel.objects.filter(admission=self).aggregate(Sum('amount'))['amount__sum']
        return payment if payment else 0
    
    def amount_waved(self):
        payment = AdmissionPaymentModel.objects.filter(admission=self).aggregate(Sum('waved_fee'))['waved_fee__sum']
        return payment if payment else 0

    def balance(self):
        balance = self.total_cost() - self.amount_paid() - self.amount_waved()
        if balance < 0:
            return 0
        return balance


class AdmissionPaymentModel(models.Model):
    """"""
    admission = models.ForeignKey(AdmissionModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    waved_fee = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.admission.patient.__str__()


class DeliveryModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    ward = models.ForeignKey(WardModel, on_delete=models.SET_NULL, null=True, blank=True)
    bed = models.ForeignKey(BedModel, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    discharge_date = models.DateField(blank=True, null=True)
    STATUS = (('active', 'ACTIVE'), ('discharged', 'DISCHARGED'))
    status = models.CharField(max_length=50, choices=STATUS, blank=True, default='active')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    discharge_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='discharge_user')
    discharge_note = models.TextField(blank=True, null=True)
    patient_status = models.CharField(max_length=20, choices=MORTALITY_STATUS, default='alive', blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def total_cost(self):
        today = timezone.now().date()
        if self.status == 'active':
            days_admitted = (today - self.date).days + 1
        else:
            days_admitted = (self.discharge_date - self.date).days + 1
        admission_fee = days_admitted * self.patient.delivery_price()

        return admission_fee

    def amount_paid(self):
        payment = DeliveryPaymentModel.objects.filter(delivery=self).aggregate(Sum('amount'))['amount__sum']
        return payment if payment else 0

    def amount_waved(self):
        payment = DeliveryPaymentModel.objects.filter(delivery=self).aggregate(Sum('waved_fee'))['waved_fee__sum']
        return payment if payment else 0

    def balance(self):
        balance = self.total_cost() - self.amount_paid() - self.amount_waved()
        if balance < 0:
            return 0
        return balance


class DeliveryPaymentModel(models.Model):
    """"""
    delivery = models.ForeignKey(DeliveryModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    waved_fee = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.delivery.patient.__str__()


class DeliveryBabyModel(models.Model):
    delivery = models.ForeignKey(DeliveryModel, on_delete=models.CASCADE, related_name='babies')
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=MORTALITY_STATUS, default='alive', blank=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time = models.TimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)






