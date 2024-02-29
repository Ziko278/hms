from datetime import date

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from patient.models import PatientModel, PatientIDGeneratorModel, PatientProfileModel
from django.contrib.auth.models import User


@receiver(post_save, sender=PatientModel)
def create_patient_account(sender, instance, created, **kwargs):
    patient = instance
    if created:
        username = patient.card_number
        password = User.objects.make_random_password(length=8)
        email = patient.email

        user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
        user_profile = PatientProfileModel.objects.create(user=user,  patient=patient,
                                                       default_password=password)
        user_profile.save()

        id_generator = PatientIDGeneratorModel.objects.filter(last_patient_id=patient.card_number).last()
        id_generator.status = 's'
        id_generator.save()

        registration_payment = patient.registration_payment
        if registration_payment:
            registration_payment.registration_status = 'completed'
            registration_payment.save()


