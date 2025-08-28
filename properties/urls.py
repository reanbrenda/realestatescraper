from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('properties/', views.PropertyListView.as_view(), name='property-list'),
    path('properties/create/', views.PropertyCreateView.as_view(), name='property-create'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('properties/<int:pk>/update/', views.PropertyUpdateView.as_view(), name='property-update'),
    path('properties/<int:pk>/delete/', views.PropertyDetailView.as_view(), name='property-delete'),
    path('properties/<int:property_id>/', views.patch_property, name='property-patch'),
    path('properties/reference/<str:reference>/', views.get_property_by_reference, name='property-by-reference'),
    path('properties/regions/', views.get_all_regions, name='all-regions'),
    
    # Bot control endpoints
    path('bot/scrapers/', views.get_bot_scrapers, name='bot-scrapers'),
    path('bot/run/', views.run_bot_scraper, name='run-bot-scraper'),
    path('bot/run-all/', views.run_all_scrapers, name='run-all-scrapers'),
]
