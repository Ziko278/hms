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


class NoteModel(models.Model):
    subject = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)


class SMTPConfigurationModel(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    host = models.CharField(max_length=200)
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()


class CommunicationSettingModel(models.Model):
    default_smtp = models.ForeignKey(SMTPConfigurationModel, on_delete=models.SET_NULL, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)


class EmailModel(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.ForeignKey(StaffModel, on_delete=models.CASCADE, blank=True, related_name='email_sender')
    receiver = models.JSONField()
    staff = models.ManyToManyField(StaffModel, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class ContactCategoryModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name.upper()


class ContactModel(models.Model):
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    category = models.ForeignKey(ContactCategoryModel, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.full_name.upper()

    def formatted_phone_number(self):
        return self.phone_number


class MessageModel(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(StaffModel, on_delete=models.CASCADE, blank=True, related_name='sender')
    receiver = models.ForeignKey(StaffModel, on_delete=models.CASCADE, blank=True, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


