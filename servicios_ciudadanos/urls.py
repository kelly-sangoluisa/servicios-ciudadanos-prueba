"""
URL configuration for servicios_ciudadanos project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def redirect_to_login(request):
    return redirect('login_ciudadano')

urlpatterns = [
    path('', include('shared.urls'), name='shared'),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('ciudadano/', include('ciudadano_app.urls'), name='ciudadano'),
    path('entidad_municipal/', include('entidad_municipal_app.urls'), name='entidad_municipal'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
