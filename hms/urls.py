from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('site-admin/', include('admin_site.urls')),
    path('', include('website.urls')),
    path('site-admin/communication/', include('communication.urls')),
    path('site-admin/laboratory/', include('laboratory.urls')),
    path('site-admin/patient/', include('patient.urls')),
    path('site-admin/human-resource/', include('human_resource.urls')),
    path('site-admin/inventory/', include('inventory.urls')),
    path('site-admin/consultation/', include('consultation.urls')),
    path('site-admin/pharmacy/', include('pharmacy.urls')),
    path('site-admin/finance/', include('finance.urls')),
    path('site-admin/user-management/', include('user_management.urls')),
    path('django-admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


