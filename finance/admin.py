from django.contrib import admin
from finance.models import RegistrationPaymentModel, IncomeModel, ExpenseModel, PaymentRemittanceModel


admin.site.register(RegistrationPaymentModel)
admin.site.register(IncomeModel)
admin.site.register(ExpenseModel)
admin.site.register(PaymentRemittanceModel)

