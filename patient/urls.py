from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from patient.views import *


urlpatterns = [
    path('register', PatientCreateView.as_view(), name='patient_create'),
    path('index', PatientListView.as_view(), name='patient_index'),
    path('returning-patient/index', ReturningPatientListView.as_view(), name='returning_patient_index'),
    path('pending-registration/index', PatientPendingListView.as_view(), name='pending_patient_index'),
    path('<int:pk>/detail', PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/edit', PatientUpdateView.as_view(), name='patient_edit'),
    path('<int:pk>/delete', PatientDeleteView.as_view(), name='patient_delete'),

    path('get-detail-with-card-number', get_patient_with_card, name='get_patient_with_card'),

    path('vitals/record', PatientVitalsCreateView.as_view(), name='patient_vitals_create'),
    path('vitals/<int:pk>/update', PatientVitalsUpdateView.as_view(), name='patient_vitals_edit'),


]
