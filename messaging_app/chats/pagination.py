from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    Fetches 20 messages per page as specified.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100