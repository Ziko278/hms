from django.urls import path
from human_resource.views import *

urlpatterns = [

    path('department/create', DepartmentCreateView.as_view(), name='department_create'),
    path('department/index', DepartmentListView.as_view(), name='department_index'),
    path('department/<int:pk>/edit', DepartmentUpdateView.as_view(), name='department_edit'),
    path('department/<int:pk>/delete', DepartmentDeleteView.as_view(), name='department_delete'),
    path('department/multi-action', multi_department_action, name='multi_department_action'),

    path('position/create', PositionCreateView.as_view(), name='position_create'),
    path('position/index', PositionListView.as_view(), name='position_index'),
    path('position/<int:pk>/edit', PositionUpdateView.as_view(), name='position_edit'),
    path('position/<int:pk>/delete', PositionDeleteView.as_view(), name='position_delete'),
    path('position/multi-action', multi_position_action, name='multi_position_action'),

    path('staff/create', StaffCreateView.as_view(), name='staff_create'),
    path('staff/index', StaffListView.as_view(), name='staff_index'),
    path('staff/<int:pk>/detail', StaffDetailView.as_view(), name='staff_detail'),
    path('staff/<int:pk>/edit', StaffUpdateView.as_view(), name='staff_edit'),
    path('staff/<int:pk>/delete', StaffDeleteView.as_view(), name='staff_delete'),

    path('staff-certificate/create', StaffCertificateCreateView.as_view(), name='staff_certificate_create'),
    path('staff-certificate/<int:pk>/edit', StaffCertificateUpdateView.as_view(), name='staff_certificate_edit'),
    path('staff-certificate/<int:pk>/delete', StaffCertificateDeleteView.as_view(), name='staff_certificate_delete'),

    path('staff-shift/<int:pk>/add', add_shift_view, name='add_shift'),

]

