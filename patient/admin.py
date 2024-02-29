from django.contrib import admin
from patient.models import PatientModel, PatientSettingModel, PatientVitalsModel


admin.site.register(PatientModel)
admin.site.register(PatientSettingModel)
admin.site.register(PatientVitalsModel)

