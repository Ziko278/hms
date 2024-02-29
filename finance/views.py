from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from consultation.models import ConsultationPaymentModel, ConsultationTestModel
from finance.models import *
from finance.forms import *
from django.db.models import Sum
from admin_site.model_info import INSURANCE_PROVIDER
from patient.models import PatientModel


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
    permission_required = 'finance.change_patientregistrationfeemodel'
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
    permission_required = 'finance.delete_patientregistrationfeemodel'
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


class InitializePaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/payment/initialize.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_type_list'] = PatientRegistrationFeeModel.objects.all()
        return context


def take_payment(request):
    if request.method == 'GET':
        messages.error(request, 'METHOD NOT ALLOWED, PERMISSION DENIED')
        return redirect(reverse('initialize_payment'))

    payment_type = request.POST.get('payment_type', '')
    if payment_type == 'registration':
        registration_type_pk = request.POST.get('registration_type')
        registration_type = PatientRegistrationFeeModel.objects.get(pk=registration_type_pk)
        amount = float(request.POST.get('amount'))
        full_name = request.POST.get('full_name')

        reg_payment = RegistrationPaymentModel.objects.create(full_name=full_name, amount=amount,
                                                              registration_type=registration_type,
                                                              registration_status='pending')
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
                                                                       amount_paid=amount, attendant=request.user)
        consultation_payment.save()
        if consultation_payment.id:
            messages.success(request, 'PAYMENT SUCCESSFUL')
            return redirect(reverse('finance_consultation_payment_index'))
        messages.error(request, 'ERROR MAKING PAYMENT! TRY AGAIN')
        return redirect(reverse('take_payment'))

    return HttpResponse('')


def patient_test_list_view(request, pk):
    patient = get_object_or_404(PatientModel, pk=pk)
    patient_test_list = ConsultationTestModel.objects.filter(patient=patient).order_by('created_at').reverse()
    context = {
        'patient': patient,
        'patient_test_list': patient_test_list
    }
    return render(request, 'finance/payment/patient_test_list.html', context)


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
                test.save()
        messages.success(request, 'Payment Successfully Recorded')
        return redirect(reverse('finance_test_payment_index'))

    context = {
        'test': test
    }
    return render(request, 'finance/payment/test_payment.html', context)


class RegistrationPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RegistrationPaymentModel
    permission_required = 'finance.view_registrationpaymentmodel'
    fields = '__all__'
    template_name = 'finance/payment/registration_payment_index.html'
    context_object_name = "registration_payment_list"

    def get_queryset(self):
        return RegistrationPaymentModel.objects.all().order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PatientRegistrationFeeForm
        context['insurance_provider_list'] = INSURANCE_PROVIDER
        return context


class ConsultationPaymentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ConsultationPaymentModel
    permission_required = 'consultation.view_consultationpaymentmodel'
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
    permission_required = 'consultation.view_consultationpaymentmodel'
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


class ExpenseCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ExpenseCategoryModel
    form_class = ExpenseCategoryForm
    success_message = 'Expense Category Added Successfully'
    template_name = 'finance/expense_category/index.html'

    def get_success_url(self):
        return reverse('expense_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        return context


class ExpenseCategoryListView(ListView):
    model = ExpenseCategoryModel
    fields = '__all__'
    template_name = 'finance/expense_category/index.html'
    context_object_name = "expense_category_list"

    def get_queryset(self):
        return ExpenseCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExpenseCategoryForm

        return context


class ExpenseCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpenseCategoryModel
    form_class = ExpenseCategoryForm
    success_message = 'Expense Category Updated Successfully'
    template_name = 'finance/expense_category/index.html'

    def get_success_url(self):
        return reverse('expense_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_category_list'] = ExpenseCategoryModel.objects.all().order_by('name')

        return context


class ExpenseCategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = ExpenseCategoryModel
    success_message = 'Expense Category Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense_category/delete.html'
    context_object_name = "expense_category"

    def get_success_url(self):
        return reverse("expense_category_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseTypeCreateView(SuccessMessageMixin, CreateView):
    model = ExpenseTypeModel
    form_class = ExpenseTypeForm
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


class ExpenseTypeListView(ListView):
    model = ExpenseTypeModel
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


class ExpenseTypeUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpenseTypeModel
    form_class = ExpenseTypeForm
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


class ExpenseTypeDeleteView(SuccessMessageMixin, DeleteView):
    model = ExpenseTypeModel
    success_message = 'Expense Type Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense_type/delete.html'
    context_object_name = "expense_type"

    def get_success_url(self):
        return reverse("expense_type_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseCreateView(SuccessMessageMixin, CreateView):
    model = ExpenseModel
    form_class = ExpenseForm
    success_message = 'Expense Added Successfully'
    template_name = 'finance/expense/create.html'

    def get_success_url(self):
        return reverse('expense_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = ExpenseCategoryModel.objects.all().order_by('name')
        return context


class ExpenseListView(ListView):
    model = ExpenseModel
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


class ExpenseDetailView(DetailView):
    model = ExpenseModel
    fields = '__all__'
    template_name = 'finance/expense/detail.html'
    context_object_name = "expense"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ExpenseUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpenseModel
    form_class = ExpenseForm
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


class ExpenseDeleteView(SuccessMessageMixin, DeleteView):
    model = ExpenseModel
    success_message = 'Expense Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/expense/delete.html'
    context_object_name = "expense"

    def get_success_url(self):
        return reverse("expense_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeCategoryCreateView(SuccessMessageMixin, CreateView):
    model = IncomeCategoryModel
    form_class = IncomeCategoryForm
    success_message = 'Income Category Added Successfully'
    template_name = 'finance/income_category/index.html'

    def get_success_url(self):
        return reverse('income_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income_category_list'] = IncomeCategoryModel.objects.all().order_by('name')
        return context


class IncomeCategoryListView(ListView):
    model = IncomeCategoryModel
    fields = '__all__'
    template_name = 'finance/income_category/index.html'
    context_object_name = "income_category_list"

    def get_queryset(self):
        return IncomeCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IncomeCategoryForm
        return context


class IncomeCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = IncomeCategoryModel
    form_class = IncomeCategoryForm
    success_message = 'Income Category Updated Successfully'
    template_name = 'finance/income_category/index.html'

    def get_success_url(self):
        return reverse('income_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income_category_list'] = IncomeCategoryModel.objects.all().order_by('name')
        return context


class IncomeCategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = IncomeCategoryModel
    success_message = 'Income Category Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/income_category/delete.html'
    context_object_name = "income_category"

    def get_success_url(self):
        return reverse("income_category_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeCreateView(SuccessMessageMixin, CreateView):
    model = IncomeModel
    form_class = IncomeForm
    success_message = 'Income Added Successfully'
    template_name = 'finance/income/create.html'

    def get_success_url(self):
        return reverse('income_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeListView(ListView):
    model = IncomeModel
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


class IncomeDetailView(DetailView):
    model = IncomeModel
    fields = '__all__'
    template_name = 'finance/income/detail.html'
    context_object_name = "income"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IncomeUpdateView(SuccessMessageMixin, UpdateView):
    model = IncomeModel
    form_class = IncomeForm
    success_message = 'Income Updated Successfully'
    template_name = 'finance/income/edit.html'

    def get_success_url(self):
        return reverse('income_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income'] = self.object
        return context


class IncomeDeleteView(SuccessMessageMixin, DeleteView):
    model = IncomeModel
    success_message = 'Income Deleted Successfully'
    fields = '__all__'
    template_name = 'finance/income/delete.html'
    context_object_name = "income"

    def get_success_url(self):
        return reverse("income_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

