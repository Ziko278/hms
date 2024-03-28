from datetime import timedelta, date, datetime
from itertools import chain
from operator import attrgetter
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.utils import timezone
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models import Q, Sum
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from admin_site.model_info import WARD_TYPE
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from consultation.models import ConsultationModel, ConsultationTestModel, ConsultationPrescriptionModel, \
    PrescriptionModel
from finance.models import AdmissionFeeModel, DeliveryFeeModel
from laboratory.models import TestModel, ConductTestResultModel, ConductTestModel
from medication.forms import SicknessForm, WardForm, BedForm, AdmissionForm, AdmissionDischargeForm, \
    DeliveryDischargeForm, DeliveryForm, DeliveryBabyForm
from medication.models import SicknessModel, WardModel, BedModel, AdmissionModel, DeliveryModel, DeliveryBabyModel
from patient.models import PatientModel


class SicknessCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = SicknessModel
    permission_required = 'medication.add_sicknessmodel'
    form_class = SicknessForm
    success_message = 'Sickness Added Successfully'
    template_name = 'medication/sickness/index.html'

    def get_success_url(self):
        return reverse('sickness_index')

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('sickness_index'))
        return super(SicknessCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sickness_list'] = SicknessModel.objects.all().order_by('name')
        return context


class SicknessListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SicknessModel
    permission_required = 'medication.add_sicknessmodel'
    fields = '__all__'
    template_name = 'medication/sickness/index.html'
    context_object_name = "sickness_list"

    def get_queryset(self):
        return SicknessModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SicknessForm
        return context


class SicknessUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SicknessModel
    permission_required = 'medication.add_sicknessmodel'
    form_class = SicknessForm
    success_message = 'Sickness Updated Successfully'
    template_name = 'medication/sickness/index.html'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('sickness_index'))
        return super(SicknessUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('sickness_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SicknessDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SicknessModel
    permission_required = 'medication.add_sicknessmodel'
    success_message = 'Sickness Deleted Successfully'
    fields = '__all__'
    template_name = 'medication/sickness/delete.html'
    context_object_name = "sickness"

    def get_success_url(self):
        return reverse('sickness_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class WardCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = WardModel
    permission_required = 'medication.add_wardmodel'
    form_class = WardForm
    success_message = 'Ward Added Successfully'
    template_name = 'medication/ward/index.html'

    def get_success_url(self):
        return reverse('ward_index')

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('ward_index'))
        return super(WardCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ward_list'] = WardModel.objects.all().order_by('name')
        return context


class WardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = WardModel
    permission_required = 'medication.add_wardmodel'
    fields = '__all__'
    template_name = 'medication/ward/index.html'
    context_object_name = "ward_list"

    def get_queryset(self):
        return WardModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = WardForm
        context['ward_type_list'] = WARD_TYPE
        return context


class WardUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = WardModel
    permission_required = 'medication.add_wardmodel'
    form_class = WardForm
    success_message = 'Ward Updated Successfully'
    template_name = 'medication/ward/index.html'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('ward_index'))
        return super(WardUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('ward_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class WardDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = WardModel
    permission_required = 'medication.add_wardmodel'
    success_message = 'Ward Deleted Successfully'
    fields = '__all__'
    template_name = 'medication/ward/delete.html'
    context_object_name = "ward"

    def get_success_url(self):
        return reverse('ward_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BedCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = BedModel
    permission_required = 'medication.add_bedmodel'
    form_class = BedForm
    success_message = 'Bed Added Successfully'
    template_name = 'medication/bed/index.html'

    def get_success_url(self):
        return reverse('bed_index')

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('bed_index'))
        return super(BedCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bed_list'] = BedModel.objects.all().order_by('name')
        return context


class BedListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BedModel
    permission_required = 'medication.add_bedmodel'
    fields = '__all__'
    template_name = 'medication/bed/index.html'
    context_object_name = "bed_list"

    def get_queryset(self):
        return BedModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BedForm
        context['ward_list'] = WardModel.objects.all().order_by('name')
        return context


class BedUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BedModel
    permission_required = 'medication.add_bedmodel'
    form_class = BedForm
    success_message = 'Bed Updated Successfully'
    template_name = 'medication/bed/index.html'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('bed_index'))
        return super(BedUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('bed_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BedDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BedModel
    permission_required = 'medication.add_bedmodel'
    success_message = 'Bed Deleted Successfully'
    fields = '__all__'
    template_name = 'medication/bed/delete.html'
    context_object_name = "bed"

    def get_success_url(self):
        return reverse('bed_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AdmissionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AdmissionModel
    permission_required = 'medication.add_admissionmodel'
    fields = '__all__'
    template_name = 'medication/admission/index.html'
    context_object_name = "admission_list"

    def get_queryset(self):
        return AdmissionModel.objects.filter(status='active').order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discharge_form'] = AdmissionDischargeForm
        return context


class DischargedAdmissionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AdmissionModel
    permission_required = 'medication.add_admissionmodel'
    fields = '__all__'
    template_name = 'medication/admission/discharged_index.html'
    context_object_name = "admission_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        return AdmissionModel.objects.filter(date__gte=start_date, date__lte=end_date, status='discharged').order_by(
        'id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        if not start_date:
            start_date = end_date = date.today()
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        context['start_date'] = start_date
        context['end_date'] = end_date
        return context


def get_admission_patient(request):
    if request.method == 'POST':
        pass
    return render(request, 'medication/admission/get_patient.html')


class AdmissionCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = AdmissionModel
    permission_required = 'medication.change_admissionmodel'
    form_class = AdmissionForm
    success_message = 'Patient Admitted Successfully'
    template_name = 'medication/admission/create.html'

    def get_success_url(self):
        return reverse('general_admission_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = PatientModel.objects.get(pk=self.request.GET.get('pk'))
        context['patient'] = patient
        patient_type = patient.insurance_provider
        if patient_type:
            context['admission_type_list'] = AdmissionFeeModel.objects.filter(insurance=patient_type)
        else:
            context['admission_type_list'] = AdmissionFeeModel.objects.filter(insurance=None)
        context['ward_list'] = WardModel.objects.all().order_by('name')
        return context


class AdmissionGeneralDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = AdmissionModel
    permission_required = 'medication.view_admissionmodel'
    fields = '__all__'
    template_name = 'medication/admission/general_detail.html'
    context_object_name = "admission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object.patient
        context['patient'] = patient
        today = timezone.now().date()

        days_admitted = (today - self.object.date).days + 1
        admission_fee = days_admitted * patient.admission_price()
        test_fee = ConductTestModel.objects.filter(
            Q(admission=self.object) & (Q(sample_collected=True) | Q(result_ready=True))
        ).aggregate(Sum('cost'))['cost__sum']
        test_fee = test_fee if test_fee else 0
        drug_fee = PrescriptionModel.objects.filter(
            Q(admission=self.object) & Q(collected=True)
        ).aggregate(Sum('total_price'))['total_price__sum']
        drug_fee = drug_fee if drug_fee else 0
        context['admission_fee'] = admission_fee
        context['test_fee'] = test_fee
        context['drug_fee'] = drug_fee
        context['total_fee'] = admission_fee + drug_fee + test_fee
        return context


class AdmissionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = AdmissionModel
    permission_required = 'medication.view_admissionmodel'
    fields = '__all__'
    template_name = 'medication/admission/detail.html'
    context_object_name = "admission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object.patient
        context['patient'] = patient
        pk = self.object.patient.pk
        consultation_list = ConsultationModel.objects.filter(patient__id=pk, admission=self.object)
        prescription_list = ConsultationPrescriptionModel.objects.filter(patient__id=pk,  admission=self.object)
        test_result_list = ConductTestResultModel.objects.filter(test__patient__id=pk, test__result_ready=True,  admission=self.object)
        consultation_test_list = ConsultationTestModel.objects.filter(patient__id=pk,  admission=self.object)
        history_list = sorted(chain(consultation_list, consultation_test_list, test_result_list, prescription_list),
                              key=attrgetter('created_at'))
        history_list.reverse()
        context['history_list'] = history_list
        context['test_list'] = TestModel.objects.all().order_by('name')
        today = timezone.now().date()

        days_admitted = (today - self.object.date).days + 1
        admission_fee = days_admitted * patient.admission_price()
        test_fee = ConductTestModel.objects.filter(
            Q(admission=self.object) & (Q(sample_collected=True) | Q(result_ready=True))
        ).aggregate(Sum('cost'))['cost__sum']
        test_fee = test_fee if test_fee else 0
        drug_fee = PrescriptionModel.objects.filter(
            Q(admission=self.object) & Q(collected=True)
        ).aggregate(Sum('total_price'))['total_price__sum']
        drug_fee = drug_fee if drug_fee else 0
        context['admission_fee'] = admission_fee
        context['test_fee'] = test_fee
        context['drug_fee'] = drug_fee
        context['total_fee'] = admission_fee + drug_fee + test_fee
        return context


class AdmissionDischargeView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AdmissionModel
    permission_required = 'medication.change_admissionmodel'
    form_class = AdmissionDischargeForm
    success_message = 'Patient Discharged Successfully'
    template_name = 'medication/admission/create.html'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('admission_index'))
        return super(AdmissionDischargeView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('general_admission_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = PatientModel.objects.get(pk=self.request.GET.get('pk'))
        context['patient'] = patient
        patient_type = patient.insurance_provider
        if patient_type:
            context['admission_type_list'] = AdmissionFeeModel.objects.filter(insurance=patient_type)
        else:
            context['admission_type_list'] = AdmissionFeeModel.objects.filter(insurance=None)
        context['ward_list'] = WardModel.objects.all().order_by('name')
        return context


class DeliveryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DeliveryModel
    permission_required = 'medication.view_deliverymodel'
    fields = '__all__'
    template_name = 'medication/delivery/index.html'
    context_object_name = "delivery_list"

    def get_queryset(self):
        return DeliveryModel.objects.filter(status='active').order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discharge_form'] = DeliveryDischargeForm
        return context


class DischargedDeliveryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DeliveryModel
    permission_required = 'medication.view_deliverymodel'
    fields = '__all__'
    template_name = 'medication/delivery/discharged_index.html'
    context_object_name = "delivery_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        return DeliveryModel.objects.filter(date__gte=start_date, date__lte=end_date, status='discharged').order_by(
        'id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        if not start_date:
            start_date = end_date = date.today()
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        context['start_date'] = start_date
        context['end_date'] = end_date
        return context


def get_delivery_patient(request):
    if request.method == 'POST':
        pass
    return render(request, 'medication/delivery/get_patient.html')


class DeliveryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DeliveryModel
    permission_required = 'medication.change_deliverymodel'
    form_class = DeliveryForm
    success_message = 'Patient Admitted Successfully'
    template_name = 'medication/delivery/create.html'

    def get_success_url(self):
        return reverse('delivery_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = PatientModel.objects.get(pk=self.request.GET.get('pk'))
        context['patient'] = patient
        patient_type = patient.insurance_provider
        if patient_type:
            context['delivery_type_list'] = DeliveryFeeModel.objects.filter(insurance=patient_type)
        else:
            context['delivery_type_list'] = DeliveryFeeModel.objects.filter(insurance=None)
        context['ward_list'] = WardModel.objects.all().order_by('name')
        return context


class DeliveryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DeliveryModel
    permission_required = 'medication.view_deliverymodel'
    fields = '__all__'
    template_name = 'medication/delivery/detail.html'
    context_object_name = "delivery"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object.patient
        context['patient'] = patient
        delivery_fee = patient.delivery_price()
        
        context['delivery_fee'] = delivery_fee 
        context['form'] = DeliveryBabyForm
        return context


class DeliveryDischargeView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DeliveryModel
    permission_required = 'medication.change_deliverymodel'
    form_class = DeliveryDischargeForm
    success_message = 'Patient Discharged Successfully'
    template_name = 'medication/delivery/create.html'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('delivery_index'))
        return super(DeliveryDischargeView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('delivery_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = PatientModel.objects.get(pk=self.request.GET.get('pk'))
        context['patient'] = patient
        patient_type = patient.insurance_provider
        if patient_type:
            context['delivery_type_list'] = DeliveryFeeModel.objects.filter(insurance=patient_type)
        else:
            context['delivery_type_list'] = DeliveryFeeModel.objects.filter(insurance=None)
        context['ward_list'] = WardModel.objects.all().order_by('name')
        return context


class DeliveryBabyCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DeliveryBabyModel
    permission_required = 'medication.change_deliverymodel'
    form_class = DeliveryBabyForm
    success_message = 'Baby Added Successfully'
    template_name = 'medication/delivery/detail.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            redirect_url = self.request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
            return redirect(redirect_url)
        return super(DeliveryBabyCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeliveryBabyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DeliveryBabyModel
    permission_required = 'medication.change_deliverymodel'
    form_class = DeliveryBabyForm
    success_message = 'Baby Detail Updated Successfully'
    template_name = 'medication/delivery/detail.html'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            redirect_url = self.request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
            return redirect(redirect_url)
        return super(DeliveryBabyUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeliveryBabyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DeliveryBabyModel
    permission_required = 'medication.change_deliverymodel'
    success_message = 'Baby Deleted Successfully'
    fields = '__all__'
    template_name = 'medication/delivery/delete_baby.html'
    context_object_name = "delivery_baby"

    def get_success_url(self):
        return reverse('delivery_detail', kwargs={'pk': self.object.delivery.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

