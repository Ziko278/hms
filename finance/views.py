from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from num2words import num2words
from consultation.models import ConsultationPaymentModel, ConsultationTestModel, ConsultationPrescriptionModel, \
    PrescriptionModel
from finance.models import *
from finance.forms import *
from django.db.models import Sum
from admin_site.model_info import INSURANCE_PROVIDER
from human_resource.models import StaffProfileModel, StaffModel
from medication.forms import AdmissionPaymentForm, DeliveryPaymentForm
from patient.models import PatientModel
from medication.models import AdmissionModel, AdmissionPaymentModel, DeliveryPaymentModel, DeliveryModel


class PatientRegistrationFeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = PatientRegistrationFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    form_class = PatientRegistrationFeeForm
    template_name = 'finance/registration_fee/index.html'
    success_message = 'Registration Fee Successfully Added'

    def get_success_url(self):
        return reverse('patient_registration_fee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class PatientRegistrationFeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PatientRegistrationFeeModel
    permission_required = 'finance.view_patientregistrationfeemodel'
    fields = '__all__'
    template_name = 'finance/registration_fee/index.html'
    context_object_name = "registration_fee_list"

    def get_queryset(self):
        return PatientRegistrationFeeModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PatientRegistrationFeeForm
        context['insurance_provider_list'] = INSURANCE_PROVIDER
        return context


class PatientRegistrationFeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PatientRegistrationFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    form_class = PatientRegistrationFeeForm
    template_name = 'finance/registration_fee/index.html'
    success_message = 'Registration Fee Successfully Updated'

    def get_success_url(self):
        return reverse('patient_registration_fee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PatientRegistrationFeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PatientRegistrationFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    fields = '__all__'
    template_name = 'finance/registration_fee/delete.html'
    context_object_name = "patient_registration_fee"
    success_message = 'Registration Fee Successfully Deleted'

    def dispatch(self, *args, **kwargs):
        if self.request.POST.get('name') in ['general']:
            messages.error(self.request, 'Restricted Fee, Permission Denied')
            return redirect(reverse('patient_registration_fee_index'))
        return super(PatientRegistrationFeeDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('patient_registration_fee_index')


class InitializePaymentView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'finance/payment/initialize.html'
    permission_required = 'finance.add_registrationpaymentmodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_type_list'] = PatientRegistrationFeeModel.objects.all()
        return context


def take_payment(request):
    if request.method == 'GET':
        messages.error(request, 'METHOD NOT ALLOWED, PERMISSION DENIED')
        return redirect(reverse('initialize_payment'))

    payment_type = request.POST.get('payment_type', '')
    user = request.user
    if payment_type == 'registration':
        registration_type_pk = request.POST.get('registration_type')
        registration_type = PatientRegistrationFeeModel.objects.get(pk=registration_type_pk)
        amount = float(request.POST.get('amount'))
        full_name = request.POST.get('full_name')

        reg_payment = RegistrationPaymentModel.objects.create(full_name=full_name, amount=amount,
                                                              registration_type=registration_type,
                                                              registration_status='pending', user=user)
        reg_payment.save()
        if reg_payment.id:
            messages.success(request, 'PAYMENT SUCCESSFUL')
            return redirect(reverse('registration_payment_index'))
    if payment_type == 'consultation':
        card_number = request.POST.get('card_number', '').strip().lower()
        try:
            patient = PatientModel.objects.get(card_number=card_number)
        except ObjectDoesNotExist:
            patient = None
        if not patient:
            messages.error(request, 'INVALID CARD NUMBER PROVIDED')
            return redirect(reverse('initialize_payment'))
        amount = patient.consultation_fee()
        consultation_payment = ConsultationPaymentModel.objects.create(patient=patient, amount=amount,
                                                                       amount_paid=amount, attendant=request.user, user=user)
        consultation_payment.save()
        if consultation_payment.id:
            messages.success(request, 'PAYMENT SUCCESSFUL')
            return redirect(reverse('finance_consultation_payment_index'))
        messages.error(request, 'ERROR MAKING PAYMENT! TRY AGAIN')
        return redirect(reverse('take_payment'))

    return HttpResponse('')


def patient_test_list_view(request, pk):
    patient = get_object_or_404(PatientModel, pk=pk)
    patient_test_list = ConsultationTestModel.objects.filter(patient=patient).exclude(admission=None).order_by('created_at').reverse()
    context = {
        'patient': patient,
        'patient_test_list': patient_test_list
    }
    return render(request, 'finance/payment/patient_test_list.html', context)


def patient_prescription_list_view(request, pk):
    patient = get_object_or_404(PatientModel, pk=pk)
    patient_prescription_list = ConsultationPrescriptionModel.objects.filter(patient=patient).order_by('created_at').reverse()
    context = {
        'patient': patient,
        'patient_prescription_list': patient_prescription_list
    }
    return render(request, 'finance/payment/patient_prescription_list.html', context)


def test_payment_view(request, pk):
    test = get_object_or_404(ConsultationTestModel, pk=pk)
    if request.method == 'POST':
        paid_test_list = request.POST.getlist('test')

        if len(paid_test_list) == 0:
            messages.error(request, 'No Test Selected')
            return redirect(reverse('test_payment', kwargs={'pk': test.pk}))
        for test in test.tests.all():
            if str(test.id) in paid_test_list:
                test.payment_made = True
                test.test_payment_user = request.user
                test.save()
        messages.success(request, 'Payment Successfully Recorded')
        return redirect(reverse('finance_test_payment_index'))

    context = {
        'test': test
    }
    return render(request, 'finance/payment/test_payment.html', context)


def prescription_payment_view(request, pk):
    prescription = get_object_or_404(ConsultationPrescriptionModel, pk=pk)
    if request.method == 'POST':
        paid_prescription_list = request.POST.getlist('prescription')

        if len(paid_prescription_list) == 0:
            messages.error(request, 'No Prescription Selected')
            return redirect(reverse('prescription_payment', kwargs={'pk': prescription.pk}))
        amount_paid = 0
        for a_prescription in prescription.prescriptions.all():
            if str(a_prescription.id) in paid_prescription_list:
                a_prescription.payment_made = True
                a_prescription.payment_user = request.user
                a_prescription.save()
                amount_paid += a_prescription.total_price

        prescription.amount_paid = amount_paid
        prescription.save()

        messages.success(request, 'Payment Successfully Recorded')
        return redirect(reverse('finance_prescription_payment_index'))

    context = {
        'prescription': prescription
    }
    return render(request, 'finance/payment/prescription_payment.html', context)


class RegistrationPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RegistrationPaymentModel
    permission_required = 'finance.view_registrationpaymentmodel'
    fields = '__all__'
    template_name = 'finance/payment/registration_payment_index.html'
    context_object_name = "registration_payment_list"

    def get_queryset(self):
        return RegistrationPaymentModel.objects.all().order_by('created_at').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PatientRegistrationFeeForm
        context['insurance_provider_list'] = INSURANCE_PROVIDER
        return context


class AdmissionPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AdmissionPaymentModel
    permission_required = 'finance.view_registrationpaymentmodel'
    fields = '__all__'
    template_name = 'finance/payment/admission_payment_index.html'
    context_object_name = "admission_payment_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        return AdmissionPaymentModel.objects.filter(date__gte=start_date, date__lte=end_date).order_by(
            'date').reverse()

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


class ConsultationPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConsultationPaymentModel
    permission_required = 'finance.view_registrationpaymentmodel'
    fields = '__all__'
    template_name = 'finance/payment/consultation_payment_index.html'
    context_object_name = "consultation_payment_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        return ConsultationPaymentModel.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date').reverse()

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


class TestPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConsultationTestModel
    permission_required = 'finance.view_registrationpaymentmodel'
    fields = '__all__'
    template_name = 'finance/payment/test_payment_index.html'
    context_object_name = "test_payment_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        return ConsultationTestModel.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date').reverse()

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


class PrescriptionPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConsultationPrescriptionModel
    permission_required = 'finance.view_registrationpaymentmodel'
    fields = '__all__'
    template_name = 'finance/payment/prescription_payment_index.html'
    context_object_name = "prescription_payment_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        return ConsultationPrescriptionModel.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date').reverse()

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


class ExpenseCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ExpenseCategoryModel
    form_class = ExpenseCategoryForm
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Expense Category Added Successfully'
    template_name = 'finance/expense_category/index.html'

    def get_success_url(self):
        return reverse('expense_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        return context


class ExpenseCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExpenseCategoryModel
    permission_required = 'finance.change_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/expense_category/index.html'
    context_object_name = "expense_category_list"

    def get_queryset(self):
        return ExpenseCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExpenseCategoryForm

        return context


class ExpenseCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ExpenseCategoryModel
    form_class = ExpenseCategoryForm
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Expense Category Updated Successfully'
    template_name = 'finance/expense_category/index.html'

    def get_success_url(self):
        return reverse('expense_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')

        return context


class ExpenseCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ExpenseCategoryModel
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Expense Category Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense_category/delete.html'
    context_object_name = "expense_category"

    def get_success_url(self):
        return reverse("expense_category_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ExpenseTypeModel
    form_class = ExpenseTypeForm
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Expense Type Added Successfully'
    template_name = 'finance/expense_type/index.html'

    def get_success_url(self):
        return reverse('expense_type_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        context['expense_type_list'] = ExpenseTypeModel.objects.all().order_by('name')
        context = super().get_context_data(**kwargs)

        return context


class ExpenseTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExpenseTypeModel
    permission_required = 'finance.change_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/expense_type/index.html'
    context_object_name = "expense_type_list"

    def get_queryset(self):
        return ExpenseTypeModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        context['form'] = ExpenseTypeForm
        return context


class ExpenseTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ExpenseTypeModel
    form_class = ExpenseTypeForm
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Expense Type Updated Successfully'
    template_name = 'finance/expense_type/index.html'

    def get_success_url(self):
        return reverse('expense_type_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        context['expense_type_list'] = ExpenseTypeModel.objects.all().order_by('name')
        context = super().get_context_data(**kwargs)

        return context


class ExpenseTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ExpenseTypeModel
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Expense Type Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense_type/delete.html'
    context_object_name = "expense_type"

    def get_success_url(self):
        return reverse("expense_type_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ExpenseModel
    form_class = ExpenseForm
    permission_required = 'finance.add_expensemodel'
    success_message = 'Expense Added Successfully'
    template_name = 'finance/expense/create.html'

    def get_success_url(self):
        return reverse('expense_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        return context


class ExpenseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ExpenseModel
    permission_required = 'finance.view_expensemodel'
    fields = '__all__'
    template_name = 'finance/expense/index.html'
    context_object_name = "expense_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())

        return ExpenseModel.objects.filter(date__gte=start_date, date__lte=end_date).order_by('category__name')

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


class ExpenseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ExpenseModel
    permission_required = 'finance.view_expensemodel'
    fields = '__all__'
    template_name = 'finance/expense/detail.html'
    context_object_name = "expense"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ExpenseModel
    form_class = ExpenseForm
    permission_required = 'finance.change_expensemodel'
    success_message = 'Expense Updated Successfully'
    template_name = 'finance/expense/edit.html'

    def get_success_url(self):
        return reverse('expense_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense'] = self.object
        context['category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        context['type_list'] = ExpenseTypeModel.objects.filter(category=self.object.category).order_by('name')
        return context


def confirm_expense(request, pk):
    # if request.user.is_superuser:
    #     messages.error(request, 'Expense Confirmation not Permitted for this User Account')
    #     redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    #     return redirect(redirect_url)

    expense = get_object_or_404(ExpenseModel, pk=pk)

    if request.method == 'POST':
        expense.status = 'confirmed'
        expense.save()
        messages.success(request, 'Expense Successfully Confirmed')
    else:
        messages.error(request, 'Method Not Supported, Permission Denied')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


class ExpenseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ExpenseModel
    permission_required = 'finance.delete_expensemodel'
    success_message = 'Expense Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense/delete.html'
    context_object_name = "expense"

    def get_success_url(self):
        return reverse("expense_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = IncomeCategoryModel
    form_class = IncomeCategoryForm
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Income Category Added Successfully'
    template_name = 'finance/income_category/index.html'

    def get_success_url(self):
        return reverse('income_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income_category_list'] = IncomeCategoryModel.objects.all().order_by('name')
        return context


class IncomeCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = IncomeCategoryModel
    permission_required = 'finance.change_financesettingmodel'
    fields = '__all__'
    template_name = 'finance/income_category/index.html'
    context_object_name = "income_category_list"

    def get_queryset(self):
        return IncomeCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IncomeCategoryForm
        return context


class IncomeCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = IncomeCategoryModel
    form_class = IncomeCategoryForm
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Income Category Updated Successfully'
    template_name = 'finance/income_category/index.html'

    def get_success_url(self):
        return reverse('income_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income_category_list'] = IncomeCategoryModel.objects.all().order_by('name')
        return context


class IncomeCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = IncomeCategoryModel
    permission_required = 'finance.change_financesettingmodel'
    success_message = 'Income Category Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/income_category/delete.html'
    context_object_name = "income_category"

    def get_success_url(self):
        return reverse("income_category_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = IncomeModel
    form_class = IncomeForm
    permission_required = 'finance.add_incomemodel'
    success_message = 'Income Added Successfully'
    template_name = 'finance/income/create.html'

    def get_success_url(self):
        return reverse('income_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = IncomeModel
    permission_required = 'finance.view_incomemodel'
    fields = '__all__'
    template_name = 'finance/income/index.html'
    context_object_name = "income_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())

        return IncomeModel.objects.filter(date__gte=start_date, date__lte=end_date).order_by('category__name')

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


class IncomeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = IncomeModel
    permission_required = 'finance.view_incomemodel'
    fields = '__all__'
    template_name = 'finance/income/detail.html'
    context_object_name = "income"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = IncomeModel
    form_class = IncomeForm
    permission_required = 'finance.change_incomemodel'
    success_message = 'Income Updated Successfully'
    template_name = 'finance/income/edit.html'

    def get_success_url(self):
        return reverse('income_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income'] = self.object
        return context


def confirm_income(request, pk):
    # if request.user.is_superuser:
    #     messages.error(request, 'Income Confirmation not Permitted for this User Account')
    #     redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    #     return redirect(redirect_url)

    income = get_object_or_404(IncomeModel, pk=pk)

    if request.method == 'POST':
        income.status = 'confirmed'
        income.save()
        messages.success(request, 'Income Successfully Confirmed')
    else:
        messages.error(request, 'Method Not Supported, Permission Denied')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


class IncomeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = IncomeModel
    permission_required = 'finance.delete_incomemodel'
    success_message = 'Income Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/income/delete.html'
    context_object_name = "income"

    def get_success_url(self):
        return reverse("income_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PendingPaymentRemittanceListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'finance.view_registrationpaymentmodel'
    template_name = 'finance/remittance/pending_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['superuser_list'] = User.objects.filter(is_superuser=True)
        context['other_staff_list'] = StaffProfileModel.objects.all()
        return context


class AllFundingListView(LoginRequiredMixin, ListView):
    model = FundingModel
    #permission_required = 'finance.view_fundingmodel'
    template_name = 'finance/funding/all_index.html'
    context_object_name = 'funding_list'

    def get_queryset(self):
        return FundingModel.objects.all().order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class MyFundingListView(LoginRequiredMixin, ListView):
    model = FundingModel
    #permission_required = 'finance.view_fundingmodel'
    template_name = 'finance/funding/my_index.html'
    context_object_name = 'funding_list'

    def get_queryset(self):
        return FundingModel.objects.filter(user=self.request.user).order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funded_list'] = FundingModel.objects.filter(confirming_user=self.request.user).order_by('id').reverse()
        return context


def add_funding_view(request):
    if request.user.is_superuser:
        messages.error(request, 'Funding not Permitted for this User Account')
        redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
        return redirect(redirect_url)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        staff_id = request.POST.get('staff')
        date = request.POST.get('date')
        staff_profile = StaffProfileModel.objects.filter(staff__id=staff_id).first()
        confirming_user = staff_profile.user
        funding = FundingModel.objects.create(user=request.user, amount=amount, confirming_user=confirming_user)
        funding.date = date if date else None
        funding.save()

        if funding.id:
            messages.success(request, 'Funding Added Successfully, Wait for Staff to Confirm Funding')
            return redirect(reverse('my_funding_index'))
        else:
            messages.error(request, 'Error Adding Funding, Try Later')
    context = {
        'staff_list': StaffModel.objects.all(),
        'form': FundingForm
    }

    return render(request, 'finance/funding/create.html', context)


def confirm_funding(request, pk):
    if request.user.is_superuser:
        messages.error(request, 'Funding not Permitted for this User Account')
        redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
        return redirect(redirect_url)

    if request.method == 'POST':
        funding = get_object_or_404(FundingModel, pk=pk)
        if funding.confirming_user != request.user:
            messages.error(request, 'Permission Denied, This action cannot be performed by current user')
        else:
            funding.status = 'confirmed'
            funding.save()
            messages.success(request, 'Funding Successfully Confirmed')
    else:
        messages.error(request, 'Method Not Supported, Permission Denied')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


def delete_funding(request, pk):
    if request.method == 'POST':
        funding = get_object_or_404(FundingModel, pk=pk)
        if funding.user != request.user:
            messages.error(request, 'Permission Denied, This action cannot be performed by current user')
        elif funding.status != 'pending':
            messages.error(request, 'Permission Denied, Confirmed Funding cannot be deleted')
        else:
            funding.delete()
            messages.success(request, 'Funding Successfully Deleted')
    else:
        messages.error(request, 'Method Not Supported, Permission Denied')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


def remit_payment_view(request):
    if request.user.is_superuser:
        messages.error(request, 'Remittance not Permitted for this User Account')
        redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
        return redirect(redirect_url)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        remittance = PaymentRemittanceModel.objects.create(user=request.user, amount=amount)
        remittance.date = date if date else None
        remittance.save()

        if remittance.id:
            messages.success(request, 'Remittance Added Successfully, Wait for Confirmation')
            return redirect(reverse('my_remittance_index'))
        else:
            messages.error(request, 'Error Adding Remittance, Try Later')

    staff = StaffProfileModel.objects.filter(user=request.user).first().staff
    amount = staff.pending_remittance()

    context = {
        'staff': staff,
        'amount': amount,
        'amount_in_word': num2words(amount)
    }
    return render(request, 'finance/remittance/remit.html', context)


class AllRemittanceListView(LoginRequiredMixin, ListView):
    model = PaymentRemittanceModel
    #permission_required = 'finance.view_fundingmodel'
    template_name = 'finance/remittance/all_index.html'
    context_object_name = 'remittance_list'

    def get_queryset(self):
        return PaymentRemittanceModel.objects.all().order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class MyRemittanceListView(LoginRequiredMixin, ListView):
    model = PaymentRemittanceModel
    #permission_required = 'finance.view_fundingmodel'
    template_name = 'finance/remittance/my_index.html'
    context_object_name = 'remittance_list'

    def get_queryset(self):
        return PaymentRemittanceModel.objects.filter(user=self.request.user).order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funded_list'] = PaymentRemittanceModel.objects.filter(user=self.request.user).order_by('id').reverse()
        return context


def confirm_remittance(request, pk):
    if request.user.is_superuser:
        messages.error(request, 'Remittance not Permitted for this User Account')
        redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
        return redirect(redirect_url)

    remittance = get_object_or_404(PaymentRemittanceModel, pk=pk)

    if request.user == remittance.user:
        messages.error(request, 'Cannot Confirm Remittance you made by yourself')
        redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
        return redirect(redirect_url)

    if request.method == 'POST':
        if remittance.user == request.user:
            messages.error(request, 'Permission Denied, This action cannot be performed by current user')
        else:
            remittance.status = 'confirmed'
            remittance.confirming_user = request.user
            remittance.save()
            messages.success(request, 'Remittance Successfully Confirmed')
    else:
        messages.error(request, 'Method Not Supported, Permission Denied')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


def delete_remittance(request, pk):
    if request.method == 'POST':
        remittance = get_object_or_404(PaymentRemittanceModel, pk=pk)
        if remittance.user != request.user:
            messages.error(request, 'Permission Denied, This action cannot be performed by current user')
        elif remittance.status != 'pending':
            messages.error(request, 'Permission Denied, Confirmed Remittance cannot be deleted')
        else:
            remittance.delete()
            messages.success(request, 'Remittance Successfully Deleted')
    else:
        messages.error(request, 'Method Not Supported, Permission Denied')
    redirect_url = request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')
    return redirect(redirect_url)


class AdmissionFeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = AdmissionFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    form_class = AdmissionFeeForm
    template_name = 'finance/admission_fee/index.html'
    success_message = 'Admission Fee Successfully Added'

    def get_success_url(self):
        return reverse('admission_fee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class AdmissionFeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AdmissionFeeModel
    permission_required = 'finance.view_patientregistrationfeemodel'
    fields = '__all__'
    template_name = 'finance/admission_fee/index.html'
    context_object_name = "admission_fee_list"

    def get_queryset(self):
        return AdmissionFeeModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdmissionFeeForm
        context['insurance_provider_list'] = INSURANCE_PROVIDER
        return context


class AdmissionFeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AdmissionFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    form_class = AdmissionFeeForm
    template_name = 'finance/admission_fee/index.html'
    success_message = 'Admission Fee Successfully Updated'

    def get_success_url(self):
        return reverse('admission_fee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AdmissionFeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AdmissionFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    fields = '__all__'
    template_name = 'finance/admission_fee/delete.html'
    context_object_name = "admission_fee"
    success_message = 'Admission Fee Successfully Deleted'

    def dispatch(self, *args, **kwargs):
        if self.request.POST.get('name', '').lower().strip() in ['general']:
            messages.error(self.request, 'Restricted Fee, Permission Denied')
            return redirect(reverse('admission_fee_index'))
        return super(AdmissionFeeDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('admission_fee_index')


class DeliveryFeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DeliveryFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    form_class = DeliveryFeeForm
    template_name = 'finance/delivery_fee/index.html'
    success_message = 'Delivery Fee Successfully Added'

    def get_success_url(self):
        return reverse('delivery_fee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DeliveryFeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DeliveryFeeModel
    permission_required = 'finance.view_patientregistrationfeemodel'
    fields = '__all__'
    template_name = 'finance/delivery_fee/index.html'
    context_object_name = "delivery_fee_list"

    def get_queryset(self):
        return DeliveryFeeModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DeliveryFeeForm
        context['insurance_provider_list'] = INSURANCE_PROVIDER
        return context


class DeliveryFeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DeliveryFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    form_class = DeliveryFeeForm
    template_name = 'finance/delivery_fee/index.html'
    success_message = 'Delivery Fee Successfully Updated'

    def get_success_url(self):
        return reverse('delivery_fee_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeliveryFeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DeliveryFeeModel
    permission_required = 'finance.add_patientregistrationfeemodel'
    fields = '__all__'
    template_name = 'finance/delivery_fee/delete.html'
    context_object_name = "delivery_fee"
    success_message = 'Delivery Fee Successfully Deleted'

    def dispatch(self, *args, **kwargs):
        if self.request.POST.get('name', '').lower().strip() in ['general']:
            messages.error(self.request, 'Restricted Fee, Permission Denied')
            return redirect(reverse('delivery_fee_index'))
        return super(DeliveryFeeDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('delivery_fee_index')


class AdmissionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AdmissionModel
    permission_required = 'medication.add_admissionmodel'
    fields = '__all__'
    template_name = 'finance/admission/index.html'
    context_object_name = "admission_list"

    def get_queryset(self):
        return AdmissionModel.objects.filter(status='active').order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class AdmissionPaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = AdmissionPaymentModel
    permission_required = 'finance.add_registrationpaymentmodel'
    form_class = AdmissionPaymentForm
    template_name = 'finance/admission_fee/index.html'
    success_message = 'Admission Fee Successfully Added'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('finance_admission_index'))
        return super(AdmissionPaymentCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('admission_payment_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    
    
class DeliveryPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DeliveryPaymentModel
    permission_required = 'finance.view_registrationpaymentmodel'
    fields = '__all__'
    template_name = 'finance/payment/delivery_payment_index.html'
    context_object_name = "delivery_payment_list"

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        return DeliveryPaymentModel.objects.filter(date__gte=start_date, date__lte=end_date).order_by(
            'date').reverse()

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


class DeliveryPaymentCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = DeliveryPaymentModel
    permission_required = 'finance.add_registrationpaymentmodel'
    form_class = DeliveryPaymentForm
    template_name = 'finance/delivery_fee/index.html'
    success_message = 'Delivery Fee Successfully Added'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('finance_delivery_index'))
        return super(DeliveryPaymentCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('delivery_payment_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DeliveryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DeliveryModel
    permission_required = 'finance.view_registrationpaymentmodel'
    fields = '__all__'
    template_name = 'finance/delivery/index.html'
    context_object_name = "delivery_list"

    def get_queryset(self):
        return DeliveryModel.objects.filter(status='active').order_by('id').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

