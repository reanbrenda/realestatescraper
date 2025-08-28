from django.urls import path
from . import views

app_name = 'exports'

urlpatterns = [
    path('pdf/', views.export_properties_pdf, name='export-pdf'),
    path('csv/', views.export_properties_csv, name='export-csv'),
    path('json/', views.export_properties_json, name='export-json'),
]
