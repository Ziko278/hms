from django.urls import path
from admin_site.views import *

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('statistic/general-dashboard', GeneralProfitDashboardView.as_view(), name='general_profit_dashboard'),
    path('statistic/patient-dashboard', PatientDashboardView.as_view(), name='patient_dashboard'),

    path('site-info/create', SiteInfoCreateView.as_view(), name='site_info_create'),
    path('site-info/<int:pk>/detail', SiteInfoDetailView.as_view(), name='site_info_detail'),
    path('site-info/<int:pk>/edit', SiteInfoUpdateView.as_view(), name='site_info_edit'),

    path('general-setting/create', GeneralSettingCreateView.as_view(), name='general_setting_create'),
    path('general-setting/<int:pk>/detail', GeneralSettingDetailView.as_view(), name='general_setting_detail'),
    path('general-setting/<int:pk>/edit', GeneralSettingUpdateView.as_view(), name='general_setting_edit'),
]

