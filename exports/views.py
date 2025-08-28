from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db.models import Q
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import csv
import io
import json
from properties.models import Property


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_properties_csv(request):
    """Export properties to CSV format"""
    property_ids = request.data.get('property_ids', [])
    
    if not property_ids:
        return Response({'error': 'property_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    properties = Property.objects.filter(id__in=property_ids)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="properties.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow([
        'Reference', 'Title', 'Category', 'Price', 'Square Meters',
        'Region', 'Town', 'Bedrooms', 'Bathrooms', 'Platform',
        'Link', 'Created At'
    ])
    
    for property_obj in properties:
        writer.writerow([
            property_obj.reference,
            property_obj.title,
            property_obj.category or '',
            property_obj.price,
            property_obj.square_meters,
            property_obj.region,
            property_obj.town or '',
            property_obj.bedrooms or '',
            property_obj.bathrooms or '',
            property_obj.platform,
            property_obj.link,
            property_obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_properties_pdf(request):
    """Export properties to PDF format"""
    property_ids = request.data.get('property_ids', [])
    
    if not property_ids:
        return Response({'error': 'property_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(property_ids) > 4:
        return Response({'error': 'Maximum 4 properties allowed for PDF export'}, status=status.HTTP_400_BAD_REQUEST)
    
    properties = Property.objects.filter(id__in=property_ids)
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title = Paragraph("Properties Export", title_style)
    elements.append(title)
    elements.append(Paragraph("<br/>", styles['Normal']))
    
    data = [['Reference', 'Title', 'Price', 'Region', 'Platform']]
    
    for prop in properties:
        data.append([
            prop.reference,
            prop.title[:30] + '...' if len(prop.title) > 30 else prop.title,
            f"€{prop.price:,.0f}",
            prop.region,
            prop.platform
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="properties.pdf"'
    
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_properties_json(request):
    """Export properties to JSON format"""
    property_ids = request.data.get('property_ids', [])
    
    if not property_ids:
        return Response({'error': 'property_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    properties = Property.objects.filter(id__in=property_ids)
    serializer_data = []
    
    for property_obj in properties:
        property_data = {
            'id': property_obj.id,
            'reference': property_obj.reference,
            'title': property_obj.title,
            'category': property_obj.category,
            'price': property_obj.price,
            'square_meters': property_obj.square_meters,
            'region': property_obj.region,
            'town': property_obj.town,
            'street_address': property_obj.street_address,
            'address_city': property_obj.address_city,
            'address_state': property_obj.address_state,
            'address_country': property_obj.address_country,
            'bedrooms': property_obj.bedrooms,
            'bathrooms': property_obj.bathrooms,
            'land_area': property_obj.land_area,
            'built_up': property_obj.built_up,
            'description': property_obj.description,
            'photos': property_obj.photos,
            'main_image': property_obj.main_image,
            'features': property_obj.features,
            'platform': property_obj.platform,
            'link': property_obj.link,
            'energy_rating': property_obj.energy_rating,
            'company_id': property_obj.company_id,
            'company_name': property_obj.company_name,
            'property_created_at': property_obj.property_created_at,
            'on_off': property_obj.on_off,
            'entity_id': property_obj.entity_id,
            'created_at': property_obj.created_at.isoformat(),
            'updated_at': property_obj.updated_at.isoformat()
        }
        serializer_data.append(property_data)
    
    response = HttpResponse(json.dumps(serializer_data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="properties.json"'
    
    return response
