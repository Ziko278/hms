from django.db import models
from admin_site.model_info import *


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


class BedModel(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(WardModel, on_delete=models.CASCADE)
    last_cleaned_date = models.DateField(blank=True, null=True)
    last_cleaned_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.ward.name)

    def current_status(self):
        if self:
            return True
        return False



