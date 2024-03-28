from django.urls import path
from laboratory.views import *

urlpatterns = [

    path('test-unit/create', TestUnitCreateView.as_view(), name='test_unit_create'),
    path('test-unit/index', TestUnitListView.as_view(), name='test_unit_index'),
    path('test-unit/<int:pk>/edit', TestUnitUpdateView.as_view(), name='test_unit_edit'),
    path('test-unit/<int:pk>/delete', TestUnitDeleteView.as_view(), name='test_unit_delete'),

    path('test-observation/create', TestObservationCreateView.as_view(), name='test_observation_create'),
    path('test-observation/index', TestObservationListView.as_view(), name='test_observation_index'),
    path('test-observation/<int:pk>/edit', TestObservationUpdateView.as_view(), name='test_observation_edit'),
    path('test-observation/<int:pk>/delete', TestObservationDeleteView.as_view(), name='test_observation_delete'),


    path('test-field/create', TestFieldCreateView.as_view(), name='test_field_create'),
    path('test-field/index', TestFieldListView.as_view(), name='test_field_index'),
    path('test-field/<int:pk>/edit', TestFieldUpdateView.as_view(), name='test_field_edit'),
    path('test-field/<int:pk>/delete', TestFieldDeleteView.as_view(), name='test_field_delete'),

    path('test/create', TestCreateView.as_view(), name='test_create'),
    path('test/index', TestListView.as_view(), name='test_index'),
    path('test/<int:pk>/detail', TestDetailView.as_view(), name='test_detail'),
    path('test/<int:pk>/edit', TestUpdateView.as_view(), name='test_edit'),
    path('test/<int:pk>/delete', TestDeleteView.as_view(), name='test_delete'),

    path('test-price/create', TestPriceCreateView.as_view(), name='test_price_create'),
    path('test-price/<int:pk>/edit', TestPriceUpdateView.as_view(), name='test_price_edit'),
    path('test-price/<int:pk>/delete', TestPriceDeleteView.as_view(), name='test_price_delete'),

    path('lab-test/index', ConsultationTestListView.as_view(), name='lab_test_index'),
    path('admission/lab-test/index', AdmissionTestListView.as_view(), name='admission_lab_test_index'),
    path('lab-test/<int:pk>/detail', ConsultationTestDetailView.as_view(), name='lab_test_detail'),

    path('lab-test/<int:pk>/collect-sample', test_sample_collection_view, name='lab_test_sample'),
    path('lab-test/<int:pk>/test-result', test_result_record_view, name='lab_test_result'),
    path('lab-test/<int:pk>/test-result/print', print_test_result_view, name='print_test_result')

]

