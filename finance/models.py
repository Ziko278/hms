from django.db import models
from django.contrib.auth.models import User, Group
from admin_site.models import GeneralSettingModel
from admin_site.model_info import *
from datetime import date
from django.apps import apps

from human_resource.models import StaffModel


def generate_payment_id():
    last_payment = PaymentIDGeneratorModel.objects.filter().last()
    if last_payment:
        payment_id = str(int(last_payment.last_id) + 1)
    else:
        payment_id = str(1)
    while True:
        gen_id = payment_id
        payment_id = 'trn' + '-' + payment_id.rjust(8, '0')
        payment_exist = ExpenseModel.objects.filter(invoice_number=payment_id).first()
        if not payment_exist:
            break
        else:
            payment_id = str(int(gen_id) + 1)

    generate_id = PaymentIDGeneratorModel.objects.create(last_id=gen_id, last_payment_id=payment_id,
                                                         status='f')
    generate_id.save()

    return payment_id


class PatientRegistrationFeeModel(models.Model):
    """"""
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    insurance = models.CharField(max_length=100, null=True, blank=True, choices=INSURANCE_PROVIDER)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_patient_reg_fee_name'
            )
        ]

    def __str__(self):
        return self.name.upper()


class RegistrationPaymentModel(models.Model):
    """"""
    full_name = models.CharField(max_length=200)
    amount = models.FloatField()
    amount_forfeited = models.FloatField(default=0)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    registration_type = models.ForeignKey(PatientRegistrationFeeModel, on_delete=models.CASCADE)
    registration_status = models.CharField(max_length=50, choices=TEMPORAL_STATUS)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.full_name.upper()

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            last_payment = RegistrationPaymentModel.objects.last()
            if last_payment:
                payment_id = last_payment.id
            else:
                payment_id = 1
            transaction_id = 'trn/reg/' + str(payment_id).rjust(6, '0')

            self.transaction_id = transaction_id

        if self.registration_type.insurance:
            general = PatientRegistrationFeeModel.objects.filter(insurance=None).first()
            if general:
                actual_price = general.amount
                self.amount_forfeited = actual_price - self.amount

        super(RegistrationPaymentModel, self).save(*args, **kwargs)


class FinanceSettingModel(models.Model):
    default_receipt_format = models.CharField(max_length=50, choices=RECEIPT_FORMAT, blank=True, null=True)


class ExpenseCategoryModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_expense_source_combo',
                violation_error_message='Expense Category Already Exists'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def no_of_expenses(self):
        return ExpenseModel.objects.filter(category=self).count()


class ExpenseTypeModel(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(ExpenseCategoryModel, on_delete=models.CASCADE, related_name='category_types')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()

    def no_of_expenses(self):
        return ExpenseModel.objects.filter(expense_type=self).count()


class ExpenseModel(models.Model):
    expense_type = models.ForeignKey(ExpenseTypeModel, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategoryModel, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    date = models.DateField(blank=True)
    expense_proof = models.FileField(upload_to='finance/expense', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = generate_payment_id()
        if not self.date:
            self.date = date.today()
        super(ExpenseModel, self).save(*args, **kwargs)


class IncomeCategoryModel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_income_category_combo',
                violation_error_message='Income Category Already Exists'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def no_of_incomes(self):
        return IncomeModel.objects.filter(category=self).count()


class IncomeModel(models.Model):
    category = models.ForeignKey(IncomeCategoryModel, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    date = models.DateTimeField(blank=True)
    income_proof = models.FileField(upload_to='finance/income', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.category.name.upper()

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()
        super(IncomeModel, self).save(*args, **kwargs)


class StaffLoanModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(blank=True, auto_now_add=True)
    confirmation_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=CONFIRMATION_STATUS, default=CONFIRMATION_STATUS[0], blank=True)
    refund_type = models.CharField(max_length=50, choices=LOAN_REFUND_TYPE, default=LOAN_REFUND_TYPE[0], blank=True)
    is_refunded = models.BooleanField(default=False)
    expected_refund_date = models.DateTimeField(blank=True, null=True)
    refund_date = models.DateTimeField(blank=True, null=True)


class StaffDeductionModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    purpose = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CONFIRMATION_STATUS, default=CONFIRMATION_STATUS[0], blank=True)
    confirmation_date = models.DateField(blank=True, null=True)


class StaffBonusModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    amount = models.FloatField()
    subject = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CONFIRMATION_STATUS, default=CONFIRMATION_STATUS[0], blank=True)
    confirmation_date = models.DateField(blank=True, null=True)


class PayrollModel(models.Model):
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE)
    salary = models.FloatField()
    loan_deduction = models.FloatField()
    other_deduction = models.FloatField()
    bonus = models.FloatField()
    payable = models.FloatField()
    date_prepared = models.DateField(auto_now_add=True)
    confirmation_date = models.DateField(blank=True, null=True)
    month = models.DateField()
    confirmation_status = models.CharField(max_length=20, choices=CONFIRMATION_STATUS, default=CONFIRMATION_STATUS[0], blank=True)
    payment_status = models.BooleanField(default=False, blank=True)


class PaymentIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_payment_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS = (
        ('s', 'SUCCESS'), ('f', 'FAIL')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, default='f')





