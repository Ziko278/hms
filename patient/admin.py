from django.contrib import admin
from patient.models import PatientModel, PatientVitalsModel, PatientMonthlyStatisticModel

admin.site.register(PatientModel)
admin.site.register(PatientVitalsModel)
admin.site.register(PatientMonthlyStatisticModel)

