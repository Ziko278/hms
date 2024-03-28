from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from consultation.models import *
from consultation.forms import *
from datetime import datetime, date
from itertools import chain
from operator import attrgetter
from django.db.models import Sum

from human_resource.models import StaffProfileModel
from pharmacy.models import *
from laboratory.models import TestModel, TestPriceModel, ConductTestResultModel
from django.db import transaction


class ConsultationBlockCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ConsultationBlockModel
    permission_required = 'human_resource.add_consultationblockmodel'
    form_class = ConsultationBlockForm
    template_name = 'consultation/block/index.html'
    success_message = 'Block Successfully Registered'

    def get_success_url(self):
        return reverse('block_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['block_list'] = ConsultationBlockModel.objects.all().order_by('name')
        return context


class ConsultationBlockListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConsultationBlockModel
    permission_required = 'consultation.view_consultationblockmodel'
    fields = '__all__'
    template_name = 'consultation/block/index.html'
    context_object_name = "block_list"

    def get_queryset(self):
        return ConsultationBlockModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ConsultationBlockForm
        return context


class ConsultationBlockUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ConsultationBlockModel
    permission_required = 'consultation.change_consultationblockmodel'
    form_class = ConsultationBlockForm
    template_name = 'consultation/block/index.html'
    success_message = 'Block Successfully Updated'

    def get_success_url(self):
        return reverse('block_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ConsultationBlockDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ConsultationBlockModel
    permission_required = 'consultation.delete_consultationblockmodel'
    fields = '__all__'
    template_name = 'consultation/block/delete.html'
    context_object_name = "consultation_block"
    success_message = 'Block Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('block_index')


class ConsultationRoomCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ConsultationRoomModel
    permission_required = 'human_resource.add_consultationroommodel'
    form_class = ConsultationRoomForm
    template_name = 'consultation/room/index.html'
    success_message = 'Room Successfully Registered'

    def get_success_url(self):
        return reverse('room_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Room_list'] = ConsultationRoomModel.objects.all().order_by('name')
        return context


class ConsultationRoomListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConsultationRoomModel
    permission_required = 'consultation.view_consultationroommodel'
    fields = '__all__'
    template_name = 'consultation/room/index.html'
    context_object_name = "room_list"

    def get_queryset(self):
        return ConsultationRoomModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ConsultationRoomForm
        context['block_list'] = ConsultationBlockModel.objects.all().order_by('name')
        return context


class ConsultationRoomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ConsultationRoomModel
    permission_required = 'consultation.change_consultationroommodel'
    form_class = ConsultationRoomForm
    template_name = 'consultation/room/index.html'
    success_message = 'Room Successfully Updated'

    def get_success_url(self):
        return reverse('room_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ConsultationRoomDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ConsultationRoomModel
    permission_required = 'consultation.delete_consultationroommodel'
    fields = '__all__'
    template_name = 'consultation/room/delete.html'
    context_object_name = "consultation_room"
    success_message = 'Room Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('room_index')


class ConsultationFeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ConsultationFeeModel
    permission_required = 'consultation.add_consultationfeemodel'
    form_class = ConsultationFeeForm
    template_name = 'consultation/fee/index.html'
    success_message = 'Consultation Fee Successfully Registered'

    def get_success_url(self):
        return reverse('consultation_fee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_list'] = ConsultationFeeModel.objects.all().order_by('name')
        return context


class ConsultationFeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConsultationFeeModel
    permission_required = 'consultation.view_consultationfeemodel'
    fields = '__all__'
    template_name = 'consultation/fee/index.html'
    context_object_name = "fee_list"

    def get_queryset(self):
        return ConsultationFeeModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ConsultationFeeForm
        context['insurance_provider_list'] = INSURANCE_PROVIDER
        context['duration_list'] = CONSULTATION_PAYMENT_DURATION
        return context


class ConsultationFeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ConsultationFeeModel
    permission_required = 'consultation.change_consultationfeemodel'
    form_class = ConsultationFeeForm
    template_name = 'consultation/fee/index.html'
    success_message = 'Consultation Fee Successfully Updated'

    def get_success_url(self):
        return reverse('consultation_fee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ConsultationFeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ConsultationFeeModel
    permission_required = 'consultation.delete_consultationFeemodel'
    fields = '__all__'
    template_name = 'consultation/fee/delete.html'
    context_object_name = "consultation_fee"
    success_message = 'Consultation Fee Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('consultation_fee_index')


class ConsultationPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConsultationPaymentModel
    permission_required = 'consultation.view_consultationfeemodel'
    fields = '__all__'
    template_name = 'consultation/consultation/payments.html'
    context_object_name = "consultation_payment_list"

    def get_queryset(self):
        today = date.today()
        return ConsultationPaymentModel.objects.filter(date=today).reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consultation_doctor_list'] = DoctorConsultationQueueModel.objects.filter(
            posting_status='active').filter(doctor_status='active')

        return context


class ConsultationDoctorListView(LoginRequiredMixin, ListView):
    model = DoctorConsultationQueueModel
    fields = '__all__'
    template_name = 'consultation/consultation/doctor_list.html'
    context_object_name = "doctor_list"

    def get_queryset(self):
        return DoctorConsultationQueueModel.objects.all().order_by('doctor__first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DoctorConsultationQueueForm
        context['block_list'] = ConsultationBlockModel.objects.all().order_by('name')
        context['room_list'] = ConsultationRoomModel.objects.all().order_by('name')
        return context


class ConsultationDoctorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DoctorConsultationQueueModel
    form_class = DoctorConsultationQueueForm
    template_name = 'consultation/consultation/doctor_list.html'
    success_message = 'Doctor Consultation detail Successfully Updated'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect('consultation_doctor_index')
        return super(ConsultationDoctorUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('consultation_doctor_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ConsultationDoctorDetailView(LoginRequiredMixin, DetailView):
    model = DoctorConsultationQueueModel
    fields = '__all__'
    template_name = 'consultation/consultation/doctor_status.html'
    context_object_name = "doctor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ConsultationDoctorStatusView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DoctorConsultationQueueModel
    form_class = DoctorConsultationStatusForm
    template_name = 'consultation/consultation/doctor_list.html'
    success_message = 'Consultation Status Successfully Updated'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect('consultation_doctor_detail', kwargs={'pk': self.object.pk})
        return super(ConsultationDoctorStatusView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('consultation_doctor_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ConsultationPatientListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = ConsultationPaymentModel
    template_name = 'consultation/consultation/previous_consultation.html'
    fields = '__all__'
    context_object_name = "consultation_list"

    def get_queryset(self):
        profile = get_object_or_404(StaffProfileModel, user=self.request.user)
        doctor = profile.staff
        # add date
        return ConsultationPaymentModel.objects.filter(doctor=doctor, is_attended=True).order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def mark_patient_as_attended(request, pk):
    consultation_payment = get_object_or_404(ConsultationPaymentModel, pk=pk)
    patient = consultation_payment.patient
    profile = get_object_or_404(StaffProfileModel, user=request.user)
    doctor = profile.staff
    queue = get_object_or_404(DoctorConsultationQueueModel, doctor=doctor)
    queue.patients.remove(patient)
    consultation_payment.is_attended = True
    consultation_payment.save()
    messages.success(request, 'Patient: {} removed from queue'.format(patient.__str__()))
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


def consultation_add_patient_view(request, payment_id, queue_id):
    payment = ConsultationPaymentModel.objects.get(pk=payment_id)
    patient = payment.patient
    queue = DoctorConsultationQueueModel.objects.get(pk=queue_id)
    doctor = queue.doctor

    if patient not in queue.patients.all():
        queue.patients.add(patient)
        payment.is_posted = True
        payment.doctor = doctor
        payment.save()

        messages.success(request, 'Patient Added to Queue')
    else:
        messages.warning(request, 'Patient Already in Queue')
    return redirect(reverse('consultation_payment_index'))


class ConsultationListView(LoginRequiredMixin, ListView):
    model = ConsultationPaymentModel
    fields = '__all__'
    template_name = 'consultation/consultation/list.html'
    context_object_name = "consultation_list"

    def get_queryset(self):
        today = date.today()
        doctor = self.request.user.user_staff_profile.staff
        return ConsultationPaymentModel.objects.filter(date=today, doctor=doctor, is_attended=False).reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ConsultationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ConsultationModel
    form_class = ConsultationForm
    template_name = 'consultation/consultation/create.html'
    success_message = 'Consultation Successfully Saved'

    def get_success_url(self):
        redirect_url = self.request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
        return redirect_url
        #return reverse('consultation_create', kwargs={'pk': self.object.patient.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['patient'] = PatientModel.objects.get(pk=pk)
        consultation_list = ConsultationModel.objects.filter(patient__id=pk, admission=None)
        prescription_list = ConsultationPrescriptionModel.objects.filter(patient__id=pk, admission=None)
        test_result_list = ConductTestResultModel.objects.filter(test__patient__id=pk, test__result_ready=True, admission=None)
        consultation_test_list = ConsultationTestModel.objects.filter(patient__id=pk, admission=None)
        history_list = sorted(chain(consultation_list, consultation_test_list, test_result_list, prescription_list), key=attrgetter('created_at'))
        history_list.reverse()
        context['history_list'] = history_list
        context['test_list'] = TestModel.objects.all().order_by('name')
        return context


class ConsultationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ConsultationModel
    form_class = ConsultationForm
    template_name = 'consultation/consultation/edit.html'
    success_message = 'Consultation Record Successfully Updated'

    def get_success_url(self):
        return reverse('consultation_create', kwargs={'pk': self.object.patient.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        context['consultation'] = self.object
        return context


class ConsultationDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ConsultationModel
    fields = '__all__'
    template_name = 'consultation/consultation/create.html'
    context_object_name = "consultation"
    success_message = 'Consultation Record Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('consultation_create', kwargs={'pk': self.object.patient.pk})


@transaction.atomic
def add_consultation_test(request):
    if request.method == "POST":
        patient_pk = request.POST.get('patient_pk', '')
        patient = PatientModel.objects.get(pk=patient_pk)
        patient_type = patient.insurance_provider
        test_list = request.POST.getlist('tests[]')
        admission_pk = request.POST.get('admission', '')
        if admission_pk:
            admission = get_object_or_404(AdmissionModel, pk=admission_pk)
        else:
            admission = None
        conducted_test_list = []
        total_cost = 0
        for test_pk in test_list:
            test = TestModel.objects.get(pk=test_pk)
            test_price = TestPriceModel.objects.filter(test=test, insurance=patient_type).first()
            if not test_price:
                test_price = TestPriceModel.objects.filter(test=test).first()

            cost = test_price.amount if test_price else 0
            total_cost += cost

            conduct_test = ConductTestModel.objects.create(test=test, patient=patient, cost=cost,
                                                           admission=admission, doctor=request.user)
            conduct_test.save()

            if conduct_test.id:
                conducted_test_list.append(conduct_test.id)

        consultation_test = ConsultationTestModel.objects.create(patient=patient, doctor=request.user,
                                                                 grand_total=total_cost, admission=admission)
        consultation_test.save()

        if consultation_test.id:
            consultation_test.tests.add(*conducted_test_list)
            consultation_test.save()

            messages.success(request, 'Test Added Successfully')
        else:
            messages.error(request, 'An Error Occurred While Adding Test, Try Later')

        redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
        return redirect(redirect_url)
        #return redirect(reverse('consultation_create', kwargs={'pk': patient.id}))


def remove_consultation_test(request, consultation_test_pk, test_pk):
    if request.method == 'POST':
        consultation_test = get_object_or_404(ConsultationTestModel, pk=consultation_test_pk)
        test = get_object_or_404(ConductTestModel, pk=test_pk)
        test_count = len(consultation_test.tests.all())
        if test.payment_made:
            messages.warning(request, 'Cannot Remove Test, Payment Already Made')
        else:
            consultation_test.tests.remove(test)
            consultation_test.save()
            messages.success(request, 'Test Removed Successfully')
            if test_count == 1:
                consultation_test.delete()
    else:
        messages.error(request, 'Method Not Allowed')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


def remove_consultation_prescription(request, consultation_prescription_pk, prescription_pk):
    if request.method == 'POST':
        consultation_prescription = get_object_or_404(ConsultationPrescriptionModel, pk=consultation_prescription_pk)
        prescription = get_object_or_404(PrescriptionModel, pk=prescription_pk)
        prescription_count = len(consultation_prescription.prescriptions.all())
        if prescription.payment_made:
            messages.warning(request, 'Cannot Remove Prescription, Payment Already Made')
        else:
            consultation_prescription.prescriptions.remove(prescription)
            consultation_prescription.save()
            messages.success(request, 'Prescription Removed Successfully')
            if prescription_count == 1:
                consultation_prescription.delete()
    else:
        messages.error(request, 'Method Not Allowed')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


@transaction.atomic
def add_consultation_prescription(request):
    if request.method == "POST":
        patient_pk = request.POST.get('patient_pk', '')
        patient = PatientModel.objects.get(pk=patient_pk)
        patient_type = patient.insurance_provider
        drug_list = request.POST.getlist('drugs')
        quantity_list = request.POST.getlist('quantity')
        admission_pk = request.POST.get('admission', '')
        if admission_pk:
            admission = get_object_or_404(AdmissionModel, pk=admission_pk)
        else:
            admission = None
        note_list = request.POST.getlist('note')
        prescribed_drug_list = []
        total_cost = 0
        for index, drug_pk in enumerate(drug_list):
            drug = DrugVariantModel.objects.get(pk=drug_pk)
            drug_price = DrugVariantPriceModel.objects.filter(drug_variant=drug, insurance=patient_type).first()
            if not drug_price:
                drug_price = DrugVariantPriceModel.objects.filter(drug_variant=drug).first()
            cost = drug_price.amount
            total_cost += cost
            quantity = float(quantity_list[index])
            note = note_list[index]
            prescribed_drug = PrescriptionModel.objects.create(drug=drug, quantity=quantity, patient=patient,
                                                               doctor=request.user, unit_selling_price=cost,
                                                               total_price=cost*quantity, dosage=note,
                                                               admission=admission)
            prescribed_drug.save()

            if prescribed_drug.id:
                prescribed_drug_list.append(prescribed_drug.id)

        consultation_prescription = ConsultationPrescriptionModel.objects.create(patient=patient, doctor=request.user,
                                                                 grand_total=total_cost, admission=admission)
        consultation_prescription.save()

        if consultation_prescription.id:
            consultation_prescription.prescriptions.add(*prescribed_drug_list)
            consultation_prescription.save()
            messages.success(request, 'Drug Prescription Added Successfully')
        else:
            messages.error(request, 'An Error Occurred While Adding Test, Try Later')

    else:
        messages.error(request, 'Method Not Allowed')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


