import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(filters.FilterSet):
    """
    Filter class for messages to retrieve conversations with specific users
    or messages within a time range.
    """
    
    # Filter for conversations with a specific user
    with_user = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        method='filter_conversations_with_user'
    )
    
    # Filter for messages within a time range
    start_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    
    # Filter for specific conversation
    conversation = filters.UUIDFilter(field_name='conversation__id')
    
    # Filter for sender
    sender = filters.ModelChoiceFilter(
        field_name='sender',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Message
        fields = ['with_user', 'start_date', 'end_date', 'conversation', 'sender']
    
    def filter_conversations_with_user(self, queryset, name, value):
        """
        Filter messages to only show those from conversations that include the specified user.
        This retrieves conversations with specific users as requested.
        """
        if value:
            # Get conversations that include both the current user and the specified user
            user_conversations = Conversation.objects.filter(
                participants=self.request.user
            ).filter(
                participants=value
            ).distinct()
            
            # Return messages from those conversations
            return queryset.filter(conversation__in=user_conversations)
        return queryset