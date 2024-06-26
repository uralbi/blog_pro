from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'  # Allow client to override, using a query param
    max_page_size = 100