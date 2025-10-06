# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    of the conversation to access (send, view, update, delete) related messages.
    """

    def has_permission(self, request, view):
        # 1. Allow only authenticated users to access the API (Method-level check)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 2. Allow only participants in a conversation to view, update, and delete messages (Object-level check)
        # This check applies to safe methods (GET/HEAD/OPTIONS) and unsafe methods (PUT/PATCH/DELETE)
        
        # The 'obj' is the Message instance being accessed.
        message = obj
        conversation = message.conversation

        # Check if the authenticated user is one of the participants.
        # This covers all methods that involve a specific message object.
        return request.user in conversation.participants.all()