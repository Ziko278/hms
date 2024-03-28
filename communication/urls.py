from django.urls import path
from communication.views import *


urlpatterns = [
    path('dashboard', CommunicationDashboardView.as_view(), name='communication_dashboard'),

    path('note/create/', NoteCreateView.as_view(), name='note_create'),
    path('note/index/', NoteListView.as_view(), name='note_index'),
    path('note/<int:pk>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),

    path('contact-category/create/', ContactCategoryCreateView.as_view(), name='contact_category_create'),
    path('contact-category/index/', ContactCategoryListView.as_view(), name='contact_category_index'),
    path('contact-category/<int:pk>/edit/', ContactCategoryUpdateView.as_view(), name='contact_category_edit'),
    path('contact-category/<int:pk>/delete/', ContactCategoryDeleteView.as_view(), name='contact_category_delete'),

    path('contact/create/', ContactCreateView.as_view(), name='contact_create'),
    path('contact/index/', ContactListView.as_view(), name='contact_index'),
    path('contact/<int:pk>/edit/', ContactUpdateView.as_view(), name='contact_edit'),
    path('contact/<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),

    path('smtp-configuration/create', SMTPConfigurationCreateView.as_view(), name='smtp_configuration_create'),
    path('smtp-configuration/index', SMTPConfigurationListView.as_view(), name='smtp_configuration_index'),
    path('smtp-configuration/<int:pk>/edit', SMTPConfigurationUpdateView.as_view(), name='smtp_configuration_edit'),
    path('smtp-configuration/<int:pk>/delete', SMTPConfigurationDeleteView.as_view(), name='smtp_configuration_delete'),

    path('communication-setting/create', CommunicationSettingCreateView.as_view(), name='communication_setting_create'),
    path('communication-setting/<int:pk>/detail', CommunicationSettingDetailView.as_view(),
         name='communication_setting_detail'),
    path('communication-setting/<int:pk>/edit', CommunicationSettingUpdateView.as_view(),
         name='communication_setting_edit'),

    path('get-staff-chat', get_staff_chat, name='get_staff_chat'),
    path('send-chat', send_chat, name='send_chat'),
    path('send-mail', send_email, name='send_mail'),
    path('send-whatsapp-message', send_whatsapp_message, name='send_whatsapp_message'),

]



