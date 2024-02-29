from django.urls import path
from website.views import *

urlpatterns = [
    path('', home_page_view, name='homepage'),
    path('about', about_page_view, name='about'),
    path('services', services_page_view, name='services'),
    path('contact-us', contact_page_view, name='contact'),
    path('subscriber-create', subscriber_view, name='subscriber'),
    path('departments/<int:pk>', departments_view, name='departments'),
    path('doctors/<int:pk>', doctors_details_view, name='doctors_details'),
    path('our-team', our_team_view, name='our_team'),
]