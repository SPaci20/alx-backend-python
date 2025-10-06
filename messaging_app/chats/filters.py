import django_filters
from django_filters import rest_framework as filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(filters.FilterSet):
    """
    Filter class for messages to retrieve conversations with specific users
    or messages within a time range.
    """
    
    # Filter for messages with a specific user (participant)
    participant = filters.ModelChoiceFilter(
        field_name='conversation__participants',
        queryset=User.objects.all(),
        method='filter_by_participant'
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
        fields = ['participant', 'start_date', 'end_date', 'conversation', 'sender']
    
    def filter_by_participant(self, queryset, name, value):
        """
        Custom method to filter messages where the specified user is a participant
        in the conversation, but exclude messages from other conversations that might
        have the same user as participant.
        """
        if value:
            return queryset.filter(conversation__participants=value)
        return queryset