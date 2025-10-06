# chats/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
import json

from .models import Message, Conversation
from .serializers import MessageSerializer, UserSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

User = get_user_model()

# Health check view (from your existing code)
@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for Kubernetes readiness and liveness probes
    """
    try:
        # Basic health check - can be expanded to check database, cache, etc.
        health_status = {
            "status": "healthy",
            "message": "Django messaging app is running",
            "service": "messaging_app"
        }
        return JsonResponse(health_status, status=200)
    except Exception as e:
        error_status = {
            "status": "unhealthy",
            "message": f"Health check failed: {str(e)}",
            "service": "messaging_app"
        }
        return JsonResponse(error_status, status=500)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Always add the current user as a participant
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Message objects.
    Enforces access control using custom permissions and queryset filtering.
    Includes pagination and filtering capabilities.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        # 1. Access the 'conversation_id' from the URL query parameters
        conversation_id = self.request.query_params.get('conversation_id')
        user = self.request.user

        # Filter to only show messages from conversations the user is a part of
        base_queryset = Message.objects.filter(
            conversation__participants=user
        ).distinct().order_by('-timestamp')  # Most recent first

        if conversation_id:
            try:
                # 2. Check if the requested conversation exists and the user is a participant
                conversation = get_object_or_404(Conversation, pk=conversation_id)
                
                if user not in conversation.participants.all():
                    # 3. Enforce access control, resulting in an HTTP_403_FORBIDDEN response
                    return HttpResponseForbidden("HTTP_403_FORBIDDEN: You are not a participant of the specified conversation.")
                
                # Filter the base queryset further for the specific conversation
                return base_queryset.filter(conversation=conversation)

            except Exception:
                # Handle cases where the conversation_id is invalid/malformed
                return base_queryset.none()
        
        # If no conversation_id is provided, return all accessible messages
        return base_queryset
    
    def perform_create(self, serializer):
        # Enforce access control when creating (sending) a message
        conversation_id = self.request.data.get('conversation')
        
        if not conversation_id:
            raise PermissionDenied("A conversation ID is required to send a message.")

        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # The permission_classes [IsParticipantOfConversation] handles the object-level check for view/update/delete.
        # This check explicitly covers the 'send' (create) action.
        if self.request.user not in conversation.participants.all():
            # Apply the access control rule for sending messages
            raise PermissionDenied("You are not authorized to send messages in this conversation.")
        
        serializer.save(sender=self.request.user, conversation=conversation)