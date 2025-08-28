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
# OpenAPI documentation removed - views no longer have schema decorators


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_properties_csv(request):
    """
    Export properties to CSV format
    
    **Request Body:**
    - property_ids (required): Array of property IDs to export
    
    **Response:**
    - CSV file download with property data
    
    **CSV Columns:**
    - Reference, Title, Category, Price, Square Meters
    - Region, Town, Bedrooms, Bathrooms, Platform
    - Link, Created At
    
    **Example Usage:**
    ```bash
    curl -X POST http://localhost:8000/api/export/csv/ \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{"property_ids": [1, 2, 3]}'
    ```
    """
    property_ids = request.data.get('property_ids', [])
    
    if not property_ids:
        return Response({'error': 'property_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get properties by IDs
    properties = Property.objects.filter(id__in=property_ids)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="properties.csv"'
    
    writer = csv.writer(response)
    
    # Write header
    writer.writerow([
        'Reference', 'Title', 'Category', 'Price', 'Square Meters',
        'Region', 'Town', 'Bedrooms', 'Bathrooms', 'Platform',
        'Link', 'Created At'
    ])
    
    # Write data
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


# OpenAPI documentation removed - schema defined in api_docs.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_properties_pdf(request):
    """
    Export properties to PDF format
    
    **Request Body:**
    - property_ids (required): Array of property IDs to export (max 4 for optimal layout)
    
    **Response:**
    - PDF file download with formatted property table
    
    **PDF Features:**
    - Professional table layout with styling
    - Limited to 4 properties for best formatting
    - Includes: Reference, Title, Price, Region, Platform
    
    **Example Usage:**
    ```bash
    curl -X POST http://localhost:8000/api/export/pdf/ \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{"property_ids": [1, 2, 3, 4]}'
    ```
    """
    property_ids = request.data.get('property_ids', [])
    
    if not property_ids:
        return Response({'error': 'property_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Limit to 4 properties like FastAPI
    limited_property_ids = property_ids[:4]
    properties = Property.objects.filter(id__in=limited_property_ids)
    
    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="properties.pdf"'
    
    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph("Properties Export", styles['Title'])
    elements.append(title)
    
    # Prepare data for table
    data = [['Reference', 'Title', 'Price', 'Region', 'Platform']]
    
    for property_obj in properties:
        data.append([
            property_obj.reference,
            property_obj.title[:50] + '...' if len(property_obj.title) > 50 else property_obj.title,
            f"€{property_obj.price:,.0f}",
            property_obj.region,
            property_obj.platform
        ])
    
    # Create table
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
    
    # Build PDF
    doc.build(elements)
    
    return response


# OpenAPI documentation removed - schema defined in api_docs.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_properties_json(request):
    """
    Export properties to JSON format
    
    **Request Body:**
    - property_ids (required): Array of property IDs to export
    
    **Response:**
    - JSON file download with complete property data
    
    **JSON Fields:**
    - reference, title, category, price, square_meters
    - region, town, bedrooms, bathrooms, platform
    - link, created_at
    
    **Example Usage:**
    ```bash
    curl -X POST http://localhost:8000/api/export/json/ \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{"property_ids": [1, 2, 3]}'
    ```
    """
    property_ids = request.data.get('property_ids', [])
    
    if not property_ids:
        return Response({'error': 'property_ids is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get properties by IDs
    properties = Property.objects.filter(id__in=property_ids)
    
    # Serialize to JSON
    data = []
    for property_obj in properties:
        data.append({
            'reference': property_obj.reference,
            'title': property_obj.title,
            'category': property_obj.category,
            'price': property_obj.price,
            'square_meters': property_obj.square_meters,
            'region': property_obj.region,
            'town': property_obj.town,
            'bedrooms': property_obj.bedrooms,
            'bathrooms': property_obj.bathrooms,
            'platform': property_obj.platform,
            'link': property_obj.link,
            'created_at': property_obj.created_at.isoformat()
        })
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="properties.json"'
    
    return response
