from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# API Documentation endpoints
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('properties.urls')),  # Property management API
    path('api/', include('users.urls')),  # Authentication API
    path('api/', include('exports.urls')),  # Export API
    
    # API Documentation - moved back under /api/ where it was working
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
