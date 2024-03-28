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

    path('admission-fee/create', AdmissionFeeCreateView.as_view(), name='admission_fee_create'),
    path('admission-fee/index', AdmissionFeeListView.as_view(), name='admission_fee_index'),
    path('admission_fee/<int:pk>/edit', AdmissionFeeUpdateView.as_view(), name='admission_fee_edit'),
    path('admission-fee/<int:pk>/delete', AdmissionFeeDeleteView.as_view(), name='admission_fee_delete'),
    
    path('delivery-fee/create', DeliveryFeeCreateView.as_view(),  name='delivery_fee_create'),
    path('delivery-fee/index', DeliveryFeeListView.as_view(), name='delivery_fee_index'),
    path('delivery_fee/<int:pk>/edit', DeliveryFeeUpdateView.as_view(), name='delivery_fee_edit'),
    path('delivery-fee/<int:pk>/delete', DeliveryFeeDeleteView.as_view(), name='delivery_fee_delete'),

    path('initialize-payment', InitializePaymentView.as_view(), name='initialize_payment'),
    path('take-payment', take_payment, name='take_payment'),
    path('laboratory-test/<int:pk>/payment', test_payment_view, name='test_payment'),
    path('prescription/<int:pk>/payment', prescription_payment_view, name='prescription_payment'),
    path('laboratory-test/<int:pk>/test-list', patient_test_list_view, name='patient_test_list'),
    path('laboratory-prescription/<int:pk>/prescription-list', patient_prescription_list_view, name='patient_prescription_list'),

    path('patient-registration-payment/index', RegistrationPaymentListView.as_view(),
         name='registration_payment_index'),
    path('patient-consultation-payment/index', ConsultationPaymentListView.as_view(),
         name='finance_consultation_payment_index'),
    path('laboratory-test-payment/index', TestPaymentListView.as_view(),
         name='finance_test_payment_index'),
    path('laboratory-prescription-payment/index', PrescriptionPaymentListView.as_view(),
         name='finance_prescription_payment_index'),

    path('income-category/create', IncomeCategoryCreateView.as_view(), name='income_category_create'),
    path('income-category/index', IncomeCategoryListView.as_view(), name='income_category_index'),
    path('income-category/<int:pk>/edit', IncomeCategoryUpdateView.as_view(), name='income_category_edit'),
    path('income-category/<int:pk>/delete', IncomeCategoryDeleteView.as_view(), name='income_category_delete'),

    path('income/create', IncomeCreateView.as_view(), name='income_create'),
    path('income/index', IncomeListView.as_view(), name='income_index'),
    path('income/<int:pk>/detail', IncomeDetailView.as_view(), name='income_detail'),
    path('income/<int:pk>/edit', IncomeUpdateView.as_view(), name='income_edit'),
    path('income/<int:pk>/confirm', confirm_income, name='income_confirm'),
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
    path('expense/<int:pk>/confirm', confirm_expense, name='expense_confirm'),
    path('expense/<int:pk>/delete', ExpenseDeleteView.as_view(), name='expense_delete'),

    path('pending-remittance/index', PendingPaymentRemittanceListView.as_view(),
         name='pending_remittance_index'),
    path('remittance/remit-payments', remit_payment_view, name='remittance_create'),
    path('remittance/all/index', AllRemittanceListView.as_view(), name='all_remittance_index'),
    path('remittance/personal/index', MyRemittanceListView.as_view(), name='my_remittance_index'),
    path('remittance/<int:pk>/confirm', confirm_remittance, name='remittance_confirm'),
    path('remittance/<int:pk>/delete', delete_remittance, name='remittance_delete'),

    path('funding/all/index', AllFundingListView.as_view(), name='all_funding_index'),
    path('funding/personal/index', MyFundingListView.as_view(), name='my_funding_index'),
    path('funding/create', add_funding_view, name='funding_create'),
    path('funding/<int:pk>/confirm', confirm_funding, name='funding_confirm'),
    path('funding/<int:pk>/delete', delete_funding, name='funding_delete'),

    path('admission/index', AdmissionListView.as_view(), name='finance_admission_index'),
    path('admission/payment/create', AdmissionPaymentCreateView.as_view(), name='admission_payment_create'),
    path('admission-payment/index', AdmissionPaymentListView.as_view(), name='admission_payment_index'),
    
    path('delivery/index', DeliveryListView.as_view(), name='finance_delivery_index'),
    path('delivery/payment/create', DeliveryPaymentCreateView.as_view(), name='delivery_payment_create'),
    path('delivery-payment/index', DeliveryPaymentListView.as_view(), name='delivery_payment_index'),

]

