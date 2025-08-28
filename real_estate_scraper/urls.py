from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_root(request):
    """API root endpoint providing information about available endpoints"""
    return JsonResponse({
        'message': 'Real Estate Scraper API',
        'version': '1.0.0',
        'endpoints': {
            'properties': '/api/properties/',
            'authentication': '/api/auth/',
            'exports': '/api/export/',
            'bot_control': '/api/bot/',
            'admin': '/admin/'
        },
        'status': 'running'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints - include all app URLs under /api/
    path('api/', include([
        path('', api_root, name='api-root'),  # API root endpoint
        path('', include('properties.urls')),  # Properties API
        path('auth/', include('users.urls')),  # Authentication API
        path('export/', include('exports.urls')),  # Export API
        
        # API Documentation - moved back under /api/ where it was working
        path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ])),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
