# chats/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from django.http import HttpResponseForbidden

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Message objects.
    """
    serializer_class = MessageSerializer
    
    # Apply custom permissions to enforce access control
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            # Although the permission_classes handle this, filtering here prevents data leakage
            return Message.objects.none()

        # If a conversation_id is passed, filter messages for that conversation
        conversation_id = self.request.query_params.get('conversation_id')
        user = self.request.user

        if conversation_id:
            # 1. Check if the user is a participant of the requested conversation
            conversation = get_object_or_404(Conversation, pk=conversation_id)
            if user not in conversation.participants.all():
                # Manually raise a 403 error for conversation filtering
                return HttpResponseForbidden("HTTP_403_FORBIDDEN: You are not a participant of this conversation.")
            
            # 2. Return messages only for that specific conversation
            # Message.objects.filter is used here
            return Message.objects.filter(conversation=conversation).order_by('timestamp')
        
        # Default: return all messages from conversations the user is a part of
        return Message.objects.filter(
            conversation__participants=user
        ).distinct().order_by('timestamp')

    def perform_create(self, serializer):
        # When sending a message (POST), check if the user is a participant of the target conversation
        conversation_id = self.request.data.get('conversation')
        if not conversation_id:
            raise PermissionDenied("Conversation ID is required to send a message.")

        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if self.request.user not in conversation.participants.all():
            # Apply the access control rule for sending messages
            raise PermissionDenied("You are not authorized to send messages in this conversation.")
        
        serializer.save(sender=self.request.user, conversation=conversation)