from django.db.models import F

from admin_site.models import GeneralSettingModel, SiteInfoModel
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from communication.models import NoteModel, RecentActivityModel
from communication.forms import NoteForm
from human_resource.models import StaffModel, StaffProfileModel
from pharmacy.models import DrugVariantModel


def general_info(request):
    hospital_info = SiteInfoModel.objects.first()
    general_setting = GeneralSettingModel.objects.first()

    try:
        note_list = NoteModel.objects.filter(user=request.user)
    except Exception:
        note_list = []

    try:
        staff_profile = StaffProfileModel.objects.filter(user=request.user).first()
        staff = staff_profile.staff
        other_staff_list = StaffModel.objects.exclude(pk=staff.pk).order_by('first_name')
    except Exception:
        other_staff_list = []
    recent_activity_list = RecentActivityModel.objects.all().order_by('id').reverse()[:15]
    low_stock_drug_list = DrugVariantModel.objects.filter(quantity__lte=F('low_limit'))

    return {
        'hospital_info': hospital_info,
        'general_setting': general_setting,
        'note_list': note_list,
        'note_form': NoteForm,
        'other_staff_list': other_staff_list,
        'layout_activity_list': recent_activity_list,
        'low_stock_drug_list': low_stock_drug_list
    }
