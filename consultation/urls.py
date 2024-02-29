from django.urls import path
from consultation.views import *

urlpatterns = [

    path('block/create', ConsultationBlockCreateView.as_view(), name='block_create'),
    path('block/index', ConsultationBlockListView.as_view(), name='block_index'),
    path('block/<int:pk>/edit', ConsultationBlockUpdateView.as_view(), name='block_edit'),
    path('block/<int:pk>/delete', ConsultationBlockDeleteView.as_view(), name='block_delete'),

    path('room/create', ConsultationRoomCreateView.as_view(), name='room_create'),
    path('room/index', ConsultationRoomListView.as_view(), name='room_index'),
    path('room/<int:pk>/edit', ConsultationRoomUpdateView.as_view(), name='room_edit'),
    path('room/<int:pk>/delete', ConsultationRoomDeleteView.as_view(), name='room_delete'),

    path('fee/create', ConsultationFeeCreateView.as_view(), name='consultation_fee_create'),
    path('fee/index', ConsultationFeeListView.as_view(), name='consultation_fee_index'),
    path('fee/<int:pk>/edit', ConsultationFeeUpdateView.as_view(), name='consultation_fee_edit'),
    path('fee/<int:pk>/delete', ConsultationFeeDeleteView.as_view(), name='consultation_fee_delete'),

    path('payment-list', ConsultationPaymentListView.as_view(), name='consultation_payment_index'),
    path('consultation-list/<int:pk>', ConsultationListView.as_view(), name='consultation_index'),

    path('patient/<int:payment_id>/add-to-queue/<int:queue_id>', consultation_add_patient_view,
         name='consultation_queue_add'),

    path('patient/<int:pk>/create', ConsultationCreateView.as_view(), name='consultation_create'),
    path('patient/<int:pk>/edit', ConsultationUpdateView.as_view(), name='consultation_edit'),
    path('patient/<int:pk>/delete', ConsultationDeleteView.as_view(), name='consultation_delete'),
    path('test/create', add_consultation_test, name='consultation_test_create'),
    path('test/<int:consultation_test_pk>/remove/<int:test_pk>', remove_consultation_test,
         name='consultation_test_remove'),
    path('prescription/create', add_consultation_prescription, name='consultation_prescription_create'),

]

