from django.contrib.auth.models import User
from django.db import models
from django.apps import apps
from patient.models import PatientModel


class UserProfileModel(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='profile')
    patient = models.OneToOneField(PatientModel, on_delete=models.CASCADE, null=True)
    default_password = models.CharField(max_length=100)

    def __str__(self):
        if self.patient:
            return self.patient.__str__()
        return "TO BE FIXED"
