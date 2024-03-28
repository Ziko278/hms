from django.db.models import Sum
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from admin_site.forms import SiteInfoForm, GeneralSettingForm
from admin_site.model_info import INSURANCE_PROVIDER
from admin_site.models import SiteInfoModel, GeneralSettingModel
from human_resource.models import StaffModel, DepartmentModel
from inventory.models import InventoryStockModel
from laboratory.models import ConductTestModel
from medication.models import AdmissionPaymentModel, DeliveryPaymentModel
from patient.models import PatientModel, PatientMonthlyStatisticModel
from communication.models import RecentActivityModel
from finance.models import ExpenseModel, IncomeModel, RegistrationPaymentModel
from consultation.models import ConsultationPaymentModel, PrescriptionModel
from datetime import date, datetime, timedelta

from pharmacy.models import DrugStockModel


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_site/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_of_patient'] = PatientModel.objects.all().count()
        today = date.today()
        expenses = ExpenseModel.objects.filter(date=today, status='confirmed')
        today_expense = 0
        expense_list = {}
        for expense in expenses:
            if expense.expense_type.__str__() not in expense_list:
                expense_list[expense.expense_type.__str__()] = expense.amount
            else:
                expense_list[expense.expense_type.__str__()] += expense.amount
            today_expense += expense.amount
        drug_expense = DrugStockModel.objects.filter(date=today).aggregate(Sum('total_cost_price'))[
            'total_cost_price__sum']
        drug_expense = drug_expense if drug_expense else 0
        today_expense += drug_expense
        expense_list['drugs'] = drug_expense

        inventory_expense = InventoryStockModel.objects.filter(date=today).aggregate(Sum('total_cost_price'))[
            'total_cost_price__sum']
        inventory_expense = inventory_expense if inventory_expense else 0
        today_expense += inventory_expense
        expense_list['inventory'] = inventory_expense
        
        incomes = IncomeModel.objects.filter(status='confirmed', date=today)
        today_income = 0
        income_list = {}
        for income in incomes:
            if income.category.__str__() not in expense_list:
                income_list[income.category.__str__()] = income.amount
            else:
                income_list[income.category.__str__()] += income.amount
            today_income += income.amount

        registration_fee = RegistrationPaymentModel.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum']
        if registration_fee is not None:
            income_list['registration'] = registration_fee
            today_income += registration_fee

        prescription_fee = PrescriptionModel.objects.filter(payment_made=True, date=today).aggregate(Sum('total_price'))[
            'total_price__sum']
        if prescription_fee is not None:
            income_list['prescription'] = prescription_fee
            today_income += prescription_fee

        admission_fee = AdmissionPaymentModel.objects.filter(date=today).aggregate(Sum('amount'))[
            'amount__sum']
        if admission_fee is not None:
            income_list['admission'] = admission_fee
            today_income += admission_fee

        delivery_fee = DeliveryPaymentModel.objects.filter(date=today).aggregate(Sum('amount'))[
            'amount__sum']
        if delivery_fee is not None:
            income_list['delivery'] = delivery_fee
            today_income += delivery_fee

        consultation_fee = ConsultationPaymentModel.objects.filter(date=today).aggregate(Sum('amount'))[
            'amount__sum']
        if consultation_fee is not None:
            income_list['consultation'] = consultation_fee
            today_income += consultation_fee

        laboratory_fee = ConductTestModel.objects.filter(payment_made=True, date=today).aggregate(Sum('cost'))[
            'cost__sum']
        if laboratory_fee is not None:
            income_list['laboratory'] = laboratory_fee
            today_income += laboratory_fee

        context['recent_activity_list'] = RecentActivityModel.objects.all().order_by('id').reverse()[:15]
        context['expense_list'] = expense_list
        context['today_expense'] = today_expense
        context['income_list'] = income_list
        context['today_income'] = today_income
        context['today_profit'] = today_income - today_expense
        total_patient = PatientModel.objects.count()
        context['number_of_patient'] = total_patient
        context['number_of_department'] = DepartmentModel.objects.count()
        context['number_of_staff'] = StaffModel.objects.count()
        worth_of_drug = DrugStockModel.objects.filter(quantity_left__gt=0).aggregate(Sum('current_worth'))[
            'current_worth__sum']
        context['worth_of_drug'] = worth_of_drug if worth_of_drug else 0
        worth_of_inventory = InventoryStockModel.objects.filter(quantity_left__gt=0).aggregate(Sum('current_worth'))[
            'current_worth__sum']
        context['worth_of_inventory'] = worth_of_inventory if worth_of_inventory else 0

        returning_patient = PatientModel.objects.filter(last_visit__year=today.year, last_visit__month=today.month).count()
        context['returning_patient'] = returning_patient
        context['returning_patient_percentage'] = round((returning_patient/total_patient) * 100) if total_patient else 0
        context['today_returning_patient_list'] = PatientModel.objects.filter(last_visit__year=today.year,
                                                                              last_visit__month=today.month,
                                                                              last_visit__day=today.day)
        current_day = 8
        start_date = datetime.now() + timedelta(days=1)
        income_7_list, expense_7_list, date_7_list, profit_7_list = [], [], [], []
        for num in range(1, 9):
            current_date = start_date - timedelta(days=current_day)
            date_7_list.append('{}'.format(current_date.strftime("%d %b")))
            all_expense = ExpenseModel.objects.filter(status='confirmed', created_at__year=current_date.year,
                                                      created_at__month=current_date.month,
                                                      created_at__day=current_date.day).aggregate(Sum('amount'))[
                'amount__sum']
            all_expense = all_expense if all_expense else 0

            expense_7_list.append(all_expense)

            all_income = IncomeModel.objects.filter(status='confirmed', created_at__year=current_date.year,
                                                    created_at__month=current_date.month,
                                                    created_at__day=current_date.day).aggregate(Sum('amount'))[
                'amount__sum']
            all_income = all_income if all_income else 0

            all_registration_fee = RegistrationPaymentModel.objects.filter(created_at__year=current_date.year,
                                                                           created_at__month=current_date.month,
                                                                           created_at__day=current_date.day).aggregate(
                Sum('amount'))[
                'amount__sum']
            all_registration_fee = all_registration_fee if all_registration_fee else 0
            all_income += all_registration_fee

            all_prescription_fee = PrescriptionModel.objects.filter(payment_made=True, created_at__year=current_date.year,
                                             created_at__month=current_date.month,
                                             created_at__day=current_date.day).aggregate(
                Sum('total_price'))[
                'total_price__sum']
            all_prescription_fee = all_prescription_fee if all_prescription_fee else 0
            all_income += all_prescription_fee

            all_admission_fee = AdmissionPaymentModel.objects.filter(created_at__year=current_date.year,
                                             created_at__month=current_date.month,
                                             created_at__day=current_date.day).aggregate(
                Sum('amount'))[
                'amount__sum']
            all_admission_fee = all_admission_fee if all_admission_fee else 0
            all_income += all_admission_fee

            all_delivery_fee = DeliveryPaymentModel.objects.filter(created_at__year=current_date.year,
                                                                     created_at__month=current_date.month,
                                                                     created_at__day=current_date.day).aggregate(
                Sum('amount'))[
                'amount__sum']
            all_delivery_fee = all_delivery_fee if all_delivery_fee else 0
            all_income += all_delivery_fee

            all_consultation_fee = ConsultationPaymentModel.objects.filter(created_at__year=current_date.year,
                                                                           created_at__month=current_date.month,
                                                                           created_at__day=current_date.day).aggregate(
                Sum('amount'))[
                'amount__sum']
            all_consultation_fee = all_consultation_fee if all_consultation_fee else 0
            all_income += all_consultation_fee

            all_laboratory_fee = ConductTestModel.objects.filter(payment_made=True, created_at__year=current_date.year,
                                                                 created_at__month=current_date.month,
                                                                 created_at__day=current_date.day).aggregate(
                Sum('cost'))[
                'cost__sum']
            all_laboratory_fee = all_laboratory_fee if all_laboratory_fee else 0
            all_income += all_laboratory_fee

            all_drug_expense = DrugStockModel.objects.filter(created_at__year=current_date.year,
                                                                 created_at__month=current_date.month,
                                                                 created_at__day=current_date.day).aggregate(Sum('total_cost_price'))[
                'total_cost_price__sum']
            all_drug_expense = all_drug_expense if all_drug_expense else 0
            all_expense += all_drug_expense

            all_inventory_expense = InventoryStockModel.objects.filter(created_at__year=current_date.year,
                                                             created_at__month=current_date.month,
                                                             created_at__day=current_date.day).aggregate(
                Sum('total_cost_price'))[
                'total_cost_price__sum']
            all_inventory_expense = all_inventory_expense if all_inventory_expense else 0
            all_expense += all_inventory_expense

            income_7_list.append(all_income)
            profit_7_list.append(all_income - all_expense)

            current_day -= 1
        context['date_7_list'] = date_7_list
        context['expense_7_list'] = expense_7_list
        context['profit_7_list'] = profit_7_list
        context['income_7_list'] = income_7_list
        context['expense_7'] = sum(expense_7_list)
        context['profit_7'] = sum(profit_7_list)
        context['income_7'] = sum(income_7_list)

        return context


class GeneralProfitDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_site/statistic/general_profit_dashboard.html'

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

        context['number_of_patient'] = PatientModel.objects.all().count()

        expenses = ExpenseModel.objects.filter(status='confirmed', date__gte=start_date, date__lte=end_date)
        total_expense = 0
        expense_list = {}
        for expense in expenses:
            if expense.expense_type.__str__() not in expense_list:
                expense_list[expense.expense_type.__str__()] = expense.amount
            else:
                expense_list[expense.expense_type.__str__()] += expense.amount
            total_expense += expense.amount

        incomes = IncomeModel.objects.filter(status='confirmed', date__gte=start_date, date__lte=end_date)
        total_income = 0
        income_list = {}
        for income in incomes:
            if income.category.__str__() not in expense_list:
                income_list[income.category.__str__()] = income.amount
            else:
                income_list[income.category.__str__()] += income.amount
            total_income += income.amount

        registration_fee = RegistrationPaymentModel.objects.filter(date__gte=start_date, date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        if registration_fee is not None:
            income_list['registration'] = registration_fee
            total_income += registration_fee

        prescription_fee = PrescriptionModel.objects.filter(payment_made=True, date__gte=start_date, date__lte=end_date).aggregate(Sum('total_price'))[
            'total_price__sum']
        if prescription_fee is not None:
            income_list['prescription'] = prescription_fee
            total_income += prescription_fee

        consultation_fee = ConsultationPaymentModel.objects.filter(date__gte=start_date, date__lte=end_date).aggregate(Sum('amount'))[
            'amount__sum']
        if consultation_fee is not None:
            income_list['consultation'] = consultation_fee
            total_income += consultation_fee

        laboratory_fee = ConductTestModel.objects.filter(payment_made=True, date__gte=start_date, date__lte=end_date).aggregate(Sum('cost'))[
            'cost__sum']
        if laboratory_fee is not None:
            income_list['laboratory'] = laboratory_fee
            total_income += laboratory_fee

        admission_fee = AdmissionPaymentModel.objects.filter(date__gte=start_date, date__lte=end_date).aggregate(Sum('amount'))[
            'amount__sum']
        if admission_fee is not None:
            income_list['admission'] = admission_fee
            total_income += admission_fee

        delivery_fee = DeliveryPaymentModel.objects.filter(date__gte=start_date, date__lte=end_date).aggregate(Sum('amount'))[
            'amount__sum']
        if delivery_fee is not None:
            income_list['delivery'] = delivery_fee
            total_income += delivery_fee

        context['recent_activity_list'] = RecentActivityModel.objects.all().order_by('id').reverse()[:15]
        context['expense_list'] = expense_list
        context['total_expense'] = total_expense
        context['income_list'] = income_list
        context['total_income'] = total_income
        context['total_profit'] = total_income - total_expense
        total_patient = PatientModel.objects.count()
        context['number_of_patient'] = total_patient
        context['number_of_department'] = DepartmentModel.objects.count()
        context['number_of_staff'] = StaffModel.objects.count()
        worth_of_drug = DrugStockModel.objects.filter(quantity_left__gt=0).aggregate(Sum('current_worth'))[
            'current_worth__sum']
        context['worth_of_drug'] = worth_of_drug if worth_of_drug else 0
        worth_of_inventory = InventoryStockModel.objects.filter(quantity_left__gt=0).aggregate(Sum('current_worth'))[
            'current_worth__sum']
        context['worth_of_inventory'] = worth_of_inventory if worth_of_inventory else 0

        current_day = 8
        start_date = datetime.now() + timedelta(days=1)
        income_7_list, expense_7_list, date_7_list, profit_7_list = [], [], [], []
        for num in range(1, 9):
            current_date = start_date - timedelta(days=current_day)
            date_7_list.append('{}'.format(current_date.strftime("%d %b")))
            all_expense = ExpenseModel.objects.filter(status='confirmed', created_at__year=current_date.year,
                                                      created_at__month=current_date.month,
                                                      created_at__day=current_date.day).aggregate(Sum('amount'))[
                'amount__sum']
            all_expense = all_expense if all_expense else 0

            all_drug_expense = DrugStockModel.objects.filter(created_at__year=current_date.year,
                                                             created_at__month=current_date.month,
                                                             created_at__day=current_date.day).aggregate(
                Sum('total_cost_price'))[
                'total_cost_price__sum']
            all_drug_expense = all_drug_expense if all_drug_expense else 0
            all_expense += all_drug_expense

            all_inventory_expense = InventoryStockModel.objects.filter(created_at__year=current_date.year,
                                                             created_at__month=current_date.month,
                                                             created_at__day=current_date.day).aggregate(
                Sum('total_cost_price'))[
                'total_cost_price__sum']
            all_inventory_expense = all_inventory_expense if all_inventory_expense else 0
            all_expense += all_inventory_expense
            
            expense_7_list.append(all_expense)

            all_income = IncomeModel.objects.filter(status='confirmed', created_at__year=current_date.year,
                                                    created_at__month=current_date.month,
                                                    created_at__day=current_date.day).aggregate(Sum('amount'))[
                'amount__sum']
            all_income = all_income if all_income else 0

            all_registration_fee = RegistrationPaymentModel.objects.filter(created_at__year=current_date.year,
                                                                           created_at__month=current_date.month,
                                                                           created_at__day=current_date.day).aggregate(
                Sum('amount'))[
                'amount__sum']
            all_registration_fee = all_registration_fee if all_registration_fee else 0
            all_income += all_registration_fee

            all_prescription_fee = PrescriptionModel.objects.filter(payment_made=True, created_at__year=current_date.year,
                                             created_at__month=current_date.month,
                                             created_at__day=current_date.day).aggregate(
                Sum('total_price'))[
                'total_price__sum']
            all_prescription_fee = all_prescription_fee if all_prescription_fee else 0
            all_income += all_prescription_fee

            all_consultation_fee = ConsultationPaymentModel.objects.filter(created_at__year=current_date.year,
                                                                           created_at__month=current_date.month,
                                                                           created_at__day=current_date.day).aggregate(
                Sum('amount'))[
                'amount__sum']
            all_consultation_fee = all_consultation_fee if all_consultation_fee else 0
            all_income += all_consultation_fee

            all_laboratory_fee = ConductTestModel.objects.filter(payment_made=True, created_at__year=current_date.year,
                                                                 created_at__month=current_date.month,
                                                                 created_at__day=current_date.day).aggregate(
                Sum('cost'))[
                'cost__sum']
            all_laboratory_fee = all_laboratory_fee if all_laboratory_fee else 0
            all_income += all_laboratory_fee

            all_admission_fee = AdmissionPaymentModel.objects.filter(created_at__year=current_date.year,
                                                                 created_at__month=current_date.month,
                                                                 created_at__day=current_date.day).aggregate(Sum('amount'))[
                'amount__sum']
            all_admission_fee = all_admission_fee if all_admission_fee else 0
            all_income += all_admission_fee

            all_delivery_fee = DeliveryPaymentModel.objects.filter(created_at__year=current_date.year,
                                                                     created_at__month=current_date.month,
                                                                     created_at__day=current_date.day).aggregate(
                Sum('amount'))[
                'amount__sum']
            all_delivery_fee = all_delivery_fee if all_delivery_fee else 0
            all_income += all_delivery_fee

            income_7_list.append(all_income)
            profit_7_list.append(all_income - all_expense)

            current_day -= 1
        context['date_7_list'] = date_7_list
        context['expense_7_list'] = expense_7_list
        context['profit_7_list'] = profit_7_list
        context['income_7_list'] = income_7_list
        context['expense_7'] = sum(expense_7_list)
        context['profit_7'] = sum(profit_7_list)
        context['income_7'] = sum(income_7_list)

        return context


class PatientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_site/statistic/patient_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = end_date = date.today()
        context['number_of_patient'] = PatientModel.objects.all().count()
        context['number_of_male_patient'] = PatientModel.objects.filter(gender='male').count()
        context['number_of_female_patient'] = PatientModel.objects.filter(gender='female').count()
        context['most_active_patient_list'] = PatientModel.objects.all().order_by('number_of_visits').reverse()[:20]
        context['patient_stat_list'] = PatientMonthlyStatisticModel.objects.all().order_by('date').reverse()[:12]
        context['current_patient_stat'] = PatientMonthlyStatisticModel.objects.filter(date__year=current_date.year, date__month=current_date.month).first()
        patient_insurance_distribution_list = {}
        for provider, provider_value in INSURANCE_PROVIDER:
            patient_insurance_distribution_list[provider] = PatientModel.objects.filter(insurance_provider=provider).count()
        patient_insurance_distribution_list['general_patient'] = PatientModel.objects.filter(insurance_provider=None).count()
        context['patient_insurance_distribution_list'] = patient_insurance_distribution_list
        context['most_active_patient'] = PatientModel.objects.order_by('number_of_visits').reverse().first()

        return context


class SiteInfoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SiteInfoModel
    form_class = SiteInfoForm
    permission_required = 'admin_site.change_siteinfomodel'
    success_message = 'Site Information Updated Successfully'
    template_name = 'admin_site/site_info/create.html'

    def dispatch(self, *args, **kwargs):
        site_info = SiteInfoModel.objects.first()
        if not site_info:
            return super(SiteInfoCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('site_info_edit', kwargs={'pk': site_info.pk}))

    def get_success_url(self):
        return reverse('site_info_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SiteInfoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = SiteInfoModel
    permission_required = 'admin_site.view_siteinfomodel'
    fields = '__all__'
    template_name = 'admin_site/site_info/detail.html'
    context_object_name = "site_info"

    def dispatch(self, *args, **kwargs):
        site_info = SiteInfoModel.objects.first()
        if site_info:
            if self.kwargs.get('pk') != site_info.id:
                return redirect(reverse('site_info_detail', kwargs={'pk': site_info.pk}))
            return super(SiteInfoDetailView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('site_info_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class SiteInfoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SiteInfoModel
    permission_required = 'admin_site.change_siteinfomodel'
    form_class = SiteInfoForm
    success_message = 'Site Information Updated Successfully'
    template_name = 'admin_site/site_info/create.html'

    def get_success_url(self):
        return reverse('site_info_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_info'] = self.object
        return context


class GeneralSettingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = GeneralSettingModel
    form_class = GeneralSettingForm
    permission_required = 'admin_site.change_generalsettingmodel'
    success_message = 'General Setting Updated Successfully'
    template_name = 'admin_site/general_setting/create.html'

    def dispatch(self, *args, **kwargs):
        site_info = GeneralSettingModel.objects.first()
        if not site_info:
            return super(GeneralSettingCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('general_setting_edit', kwargs={'pk': site_info.pk}))

    def get_success_url(self):
        return reverse('general_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GeneralSettingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = GeneralSettingModel
    permission_required = 'admin_site.change_generalsettingmodel'
    fields = '__all__'
    template_name = 'admin_site/general_setting/detail.html'
    context_object_name = "general_setting"

    def dispatch(self, *args, **kwargs):
        site_info = GeneralSettingModel.objects.first()
        if site_info:
            if self.kwargs.get('pk') != site_info.id:
                return redirect(reverse('general_setting_detail', kwargs={'pk': site_info.pk}))
            return super(GeneralSettingDetailView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('general_setting_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class GeneralSettingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = GeneralSettingModel
    form_class = GeneralSettingForm
    permission_required = 'admin_site.change_generalsettingmodel'
    success_message = 'General Setting Updated Successfully'
    template_name = 'admin_site/general_setting/create.html'

    def get_success_url(self):
        return reverse('general_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['general_setting'] = self.object
        return context

