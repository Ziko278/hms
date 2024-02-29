from django.db import models
from human_resource.models import StaffModel


class StaffAttendanceModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    attendance = models.JSONField(blank=True, null=True)
    month = models.DateField(blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    summary = models.JSONField(null=True, blank=True)
