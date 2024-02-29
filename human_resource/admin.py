from django.contrib import admin
from human_resource.models import HRSettingModel, StaffModel, StaffProfileModel


admin.site.register(HRSettingModel)
admin.site.register(StaffModel)
admin.site.register(StaffProfileModel)