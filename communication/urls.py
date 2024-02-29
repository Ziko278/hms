from django.urls import path
from communication.views import *


urlpatterns = [
    path('dashboard', CommunicationDashboardView.as_view(), name='communication_dashboard'),

]



