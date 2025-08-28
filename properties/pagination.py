from rest_framework.pagination import PageNumberPagination


class PropertyPagination(PageNumberPagination):
    """Custom pagination for properties"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
