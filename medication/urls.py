from django.urls import path
from medication.views import *

urlpatterns = [
    path('sickness/create', SicknessCreateView.as_view(), name='sickness_create'),
    path('sickness/index', SicknessListView.as_view(), name='sickness_index'),
    path('sickness/<int:pk>/edit', SicknessUpdateView.as_view(), name='sickness_edit'),
    path('sickness/<int:pk>/delete', SicknessDeleteView.as_view(), name='sickness_delete'),

    path('ward/create', WardCreateView.as_view(), name='ward_create'),
    path('ward/index', WardListView.as_view(), name='ward_index'),
    path('ward/<int:pk>/edit', WardUpdateView.as_view(), name='ward_edit'),
    path('ward/<int:pk>/delete', WardDeleteView.as_view(), name='ward_delete'),

    path('bed/create', BedCreateView.as_view(), name='bed_create'),
    path('bed/index', BedListView.as_view(), name='bed_index'),
    path('bed/<int:pk>/edit', BedUpdateView.as_view(), name='bed_edit'),
    path('bed/<int:pk>/delete', BedDeleteView.as_view(), name='bed_delete'),

    path('admission/create', AdmissionCreateView.as_view(), name='admission_create'),
    path('admission/index', AdmissionListView.as_view(), name='admission_index'),
    path('admission/<int:pk>/discharge', AdmissionDischargeView.as_view(), name='admission_discharge'),
    path('discharged-admission/index', DischargedAdmissionListView.as_view(), name='discharged_admission_index'),
    path('admission/<int:pk>/detail', AdmissionDetailView.as_view(), name='admission_detail'),
    path('admission/<int:pk>/general-detail', AdmissionGeneralDetailView.as_view(), name='general_admission_detail'),
    path('get-admission-patient', get_admission_patient, name='get_admission_patient'),

    path('delivery/create', DeliveryCreateView.as_view(), name='delivery_create'),
    path('delivery/index', DeliveryListView.as_view(), name='delivery_index'),
    path('delivery/<int:pk>/discharge', DeliveryDischargeView.as_view(), name='delivery_discharge'),
    path('discharged-delivery/index', DischargedDeliveryListView.as_view(), name='discharged_delivery_index'),
    path('delivery/<int:pk>/detail', DeliveryDetailView.as_view(), name='delivery_detail'),
    path('get-delivery-patient', get_delivery_patient, name='get_delivery_patient'),

    path('delivery-baby/create', DeliveryBabyCreateView.as_view(), name='delivery_baby_create'),
    path('delivery-baby/<int:pk>/update', DeliveryBabyUpdateView.as_view(), name='delivery_baby_edit'),
    path('delivery-baby/<int:pk>/delete', DeliveryBabyDeleteView.as_view(), name='delivery_baby_delete'),


]




