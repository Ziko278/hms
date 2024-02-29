from django.shortcuts import render
from pharmacy.models import DrugModel
from django.http import HttpResponse, JsonResponse
from patient.models import PatientModel
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from consultation.models import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from pharmacy.models import *
from pharmacy.forms import *


class CommunicationDashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'academic.add_classesmodel'
    template_name = 'communication/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
