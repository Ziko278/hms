from django.urls import path
from finance.views import *

urlpatterns = [

    path('patient-registration-fee/create', PatientRegistrationFeeCreateView.as_view(),
         name='patient_registration_fee_create'),
    path('patient-registration-fee/index', PatientRegistrationFeeListView.as_view(),
         name='patient_registration_fee_index'),
    path('patient-registration_fee/<int:pk>/edit', PatientRegistrationFeeUpdateView.as_view(),
         name='patient_registration_fee_edit'),
    path('patient-registration-fee/<int:pk>/delete', PatientRegistrationFeeDeleteView.as_view(),
         name='patient_registration_fee_delete'),

    path('initialize-payment', InitializePaymentView.as_view(), name='initialize_payment'),
    path('take-payment', take_payment, name='take_payment'),
    path('laboratory-test/<int:pk>/payment', test_payment_view, name='test_payment'),
    path('laboratory-test/<int:pk>/test-list', patient_test_list_view, name='patient_test_list'),

    path('patient-registration-payment/index', RegistrationPaymentListView.as_view(),
         name='registration_payment_index'),
    path('patient-consultation-payment/index', ConsultationPaymentListView.as_view(),
         name='finance_consultation_payment_index'),
    path('laboratory-test-payment/index', TestPaymentListView.as_view(),
         name='finance_test_payment_index'),

    path('income-category/create', IncomeCategoryCreateView.as_view(), name='income_category_create'),
    path('income-category/index', IncomeCategoryListView.as_view(), name='income_category_index'),
    path('income-category/<int:pk>/edit', IncomeCategoryUpdateView.as_view(), name='income_category_edit'),
    path('income-category/<int:pk>/delete', IncomeCategoryDeleteView.as_view(), name='income_category_delete'),

    path('income/create', IncomeCreateView.as_view(), name='income_create'),
    path('income/index', IncomeListView.as_view(), name='income_index'),
    path('income/<int:pk>/detail', IncomeDetailView.as_view(), name='income_detail'),
    path('income/<int:pk>/edit', IncomeUpdateView.as_view(), name='income_edit'),
    path('income/<int:pk>/delete', IncomeDeleteView.as_view(), name='income_delete'),

    path('expense-category/create', ExpenseCategoryCreateView.as_view(), name='expense_category_create'),
    path('expense-category/index', ExpenseCategoryListView.as_view(), name='expense_category_index'),
    path('expense-category/<int:pk>/edit', ExpenseCategoryUpdateView.as_view(), name='expense_category_edit'),
    path('expense-category/<int:pk>/delete', ExpenseCategoryDeleteView.as_view(), name='expense_category_delete'),

    path('expense-type/create', ExpenseTypeCreateView.as_view(), name='expense_type_create'),
    path('expense-type/index', ExpenseTypeListView.as_view(), name='expense_type_index'),
    path('expense-type/<int:pk>/edit', ExpenseTypeUpdateView.as_view(), name='expense_type_edit'),
    path('expense-type/<int:pk>/delete', ExpenseTypeDeleteView.as_view(), name='expense_type_delete'),

    path('expense/create', ExpenseCreateView.as_view(), name='expense_create'),
    path('expense/index', ExpenseListView.as_view(), name='expense_index'),
    path('expense/<int:pk>/detail', ExpenseDetailView.as_view(), name='expense_detail'),
    path('expense/<int:pk>/edit', ExpenseUpdateView.as_view(), name='expense_edit'),
    path('expense/<int:pk>/delete', ExpenseDeleteView.as_view(), name='expense_delete'),
]

