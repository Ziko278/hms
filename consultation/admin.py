from django.contrib import admin
from consultation.models import *


admin.site.register(ConsultationPaymentModel)
admin.site.register(DoctorConsultationQueueModel)
admin.site.register(ConductTestModel)
admin.site.register(ConsultationTestModel)
admin.site.register(ConsultationModel)