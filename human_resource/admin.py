from django.contrib import admin
from human_resource.models import StaffModel, StaffProfileModel, StaffIDGeneratorModel


admin.site.register(StaffModel)
admin.site.register(StaffProfileModel)
admin.site.register(StaffIDGeneratorModel)
