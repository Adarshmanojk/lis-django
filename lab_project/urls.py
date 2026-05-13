"""
Root URL configuration for the LIS project.
Routes traffic to the API namespace and frontend template views.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('patients.urls')),
    path('api/v1/', include('labtests.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('results.urls')),
    path('', include('accounts.frontend_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
