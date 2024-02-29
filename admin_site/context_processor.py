from admin_site.models import GeneralSettingModel, SiteInfoModel
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect


def general_info(request):
    hospital_info = SiteInfoModel.objects.first()
    general_setting = GeneralSettingModel.objects.first()

    return {
        'hospital_info': hospital_info,
        'general_setting': general_setting,
    }
