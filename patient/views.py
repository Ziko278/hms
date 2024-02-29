from itertools import chain
from operator import attrgetter
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from admin_site.utility import state_list
from consultation.models import ConsultationModel, ConsultationPrescriptionModel, ConsultationTestModel
from laboratory.models import ConductTestResultModel
from patient.models import *
from patient.forms import *
from finance.models import RegistrationPaymentModel


class PatientCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = PatientModel
    permission_required = 'patient.add_patientmodel'
    form_class = PatientForm
    template_name = 'patient/create.html'
    success_message = 'Patient Successfully Registered'

    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, *args, **kwargs):
        general_setting = GeneralSettingModel.objects.first()
        pay_id = self.request.GET.get('pay_id', '')
        if pay_id:
            payment = RegistrationPaymentModel.objects.get(pk=pay_id)
            if payment.registration_status == 'completed':
                messages.error(self.request, 'Registration for Payment Already Completed')
                return redirect(reverse('pending_patient_index'))
        if not general_setting.patient_registration_without_payment:
            if not pay_id:
                raise PermissionError('CANNOT CREATE PATIENT WITHOUT PAYMENT')
        return super(PatientCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pay_id = self.request.GET.get('pay_id', '')
        if pay_id:
            payment = RegistrationPaymentModel.objects.get(pk=pay_id)

            full_name = payment.full_name
            name_list = full_name.strip().split(" ")
            if len(name_list) == 1:
                first_name, middle_name, last_name = (name_list[0], '', '')
            elif len(name_list) == 2:
                first_name, middle_name, last_name = (name_list[0], '', name_list[1])
            else:
                first_name, middle_name, last_name = (name_list[0], name_list[1], name_list[2])
            insurance_provider = payment.registration_type.insurance
        else:
            first_name, middle_name, last_name, insurance_provider = ('', '', '', '')
        context['pay_id'] = pay_id
        context['state_list'] = state_list
        context['first_name'] = first_name
        context['middle_name'] = middle_name
        context['last_name'] = last_name
        context['patient_setting'] = PatientSettingModel.objects.filter().first()
        context['insurance_provider'] = insurance_provider
        context['insurance_provider_list'] = INSURANCE_PROVIDER
        return context


class PatientPendingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RegistrationPaymentModel
    permission_required = 'patient.view_patientmodel'
    fields = '__all__'
    template_name = 'patient/pending_index.html'
    context_object_name = "pending_payment_list"

    def get_queryset(self):
        return RegistrationPaymentModel.objects.filter(registration_status='pending').order_by('created_at').reverse()


class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PatientModel
    permission_required = 'patient.view_patientmodel'
    fields = '__all__'
    template_name = 'patient/index.html'
    context_object_name = "patient_list"

    def get_queryset(self):
        return PatientModel.objects.all().order_by('first_name')


class PatientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = PatientModel
    permission_required = 'patient.view_patientmodel'
    fields = '__all__'
    template_name = 'patient/detail.html'
    context_object_name = "patient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consultation_list = ConsultationModel.objects.filter(patient__id=self.object.pk)
        prescription_list = ConsultationPrescriptionModel.objects.filter(patient__id=self.object.pk)
        test_result_list = ConductTestResultModel.objects.filter(test__patient__id=self.object.pk)
        consultation_test_list = ConsultationTestModel.objects.filter(patient__id=self.object.pk)
        history_list = sorted(chain(consultation_list, consultation_test_list, test_result_list, prescription_list),
                              key=attrgetter('created_at'))
        history_list.reverse()
        context['history_list'] = history_list
        return context


class PatientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PatientModel
    permission_required = 'patient.change_patientmodel'
    form_class = PatientEditForm
    template_name = 'patient/edit.html'
    success_message = 'Patient Information Successfully Updated'

    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, *args, **kwargs):
        return super(PatientUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['state_list'] = state_list
        context['patient'] = self.object
        context['patient_setting'] = PatientSettingModel.objects.filter().first()
        return context


class PatientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PatientModel
    permission_required = 'patient.delete_patientmodel'
    fields = '__all__'
    template_name = 'patient/delete.html'
    context_object_name = "patient"
    success_message = 'Patient Successfully Deleted'

    def get_success_url(self):
        return reverse('patient_index')


def get_patient_with_card(request):
    card_number = request.GET.get('card_number', '')
    payment_type = request.GET.get('payment_type', '')
    try:
        patient = PatientModel.objects.get(card_number=card_number)
    except ObjectDoesNotExist:
        patient = None
    context = {
        'patient': patient,
        'payment_type': payment_type,
    }
    return render(request, 'patient/get_detail_from_card.html', context)


class PatientVitalsCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = PatientVitalsModel
    permission_required = 'patient.add_patientvitalsmodel'
    form_class = PatientVitalsForm
    template_name = 'consultation/consultation/payments.html'
    success_message = 'Patient Vitals Successfully Recorded'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'POST':
            pk = self.request.POST.get('patient', None)
            if pk:
                vital_count = PatientVitalsModel.objects.filter(patient__pk=pk).count()
                if vital_count > 5:
                    PatientVitalsModel.objects.last().delete()
        return super(PatientVitalsCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('consultation_payment_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PatientVitalsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PatientVitalsModel
    permission_required = 'patient.change_patientvitalsmodel'
    form_class = PatientVitalsForm
    template_name = 'consultation/consultation/payments.html'
    success_message = 'Patient Vitals Updated Recorded'

    def get_success_url(self):
        return reverse('consultation_payment_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

