from django.db import models
from django.contrib.auth.models import User
from human_resource.models import StaffModel
from admin_site.model_info import *


class RecentActivityModel(models.Model):
    category = models.CharField(max_length=100)
    subject = models.CharField(max_length=250)
    reference_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class SMTPConfigurationModel(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    host = models.CharField(max_length=200)
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ACTIVE_STATUS, default=ACTIVE_STATUS[0], blank=True)

    def __str__(self):
        return self.name.upper()


class CommunicationSettingModel(models.Model):
    default_smtp = models.ForeignKey(SMTPConfigurationModel, on_delete=models.SET_NULL, null=True, blank=True)
    auto_save_sent_message = models.BooleanField(default=False)


class EmailModel(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.ForeignKey(StaffModel, on_delete=models.CASCADE, blank=True, related_name='email_sender')
    receiver = models.JSONField()
    staff = models.ManyToManyField(StaffModel, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class ContactModel(models.Model):
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    extra_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class MessageModel(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.ForeignKey(StaffModel, on_delete=models.CASCADE, blank=True, related_name='sender')
    receiver = models.ForeignKey(StaffModel, on_delete=models.CASCADE, blank=True, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


