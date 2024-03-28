from django.urls import path
from user_management.views import *

urlpatterns = [
    path('group/add', GroupCreateView.as_view(), name='group_create'),
    path('group/index', GroupListView.as_view(), name='group_index'),
    path('group/<int:pk>/detail', GroupDetailView.as_view(), name='group_detail'),
    path('group/<int:pk>/edit', GroupUpdateView.as_view(), name='group_edit'),
    path('group/<int:pk>/permission/edit', group_permission_view, name='group_permission'),
    path('group/<int:pk>/delete', GroupDeleteView.as_view(), name='group_delete'),

    path('sign-in', user_sign_in_view, name='login'),
    path('sign-out', user_sign_out_view, name='logout'),
    path('change-password', user_change_password_view, name='change_password'),


]
