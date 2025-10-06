# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    of the conversation to access the related messages.
    """

    def has_permission(self, request, view):
        # Allow access only to authenticated users (initial check)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Safety check: if the user is not authenticated, deny access (though has_permission should catch this)
        if not request.user.is_authenticated:
            return False

        # For Message objects, the related object is the 'conversation'
        # The 'obj' passed here is typically a Message instance.
        message = obj
        conversation = message.conversation

        # Check if the authenticated user is one of the participants
        # Assuming the Conversation model has a 'participants' ManyToMany field
        # or a similar method/property to check for membership.
        # This implementation assumes the 'participants' field directly:
        return request.user in conversation.participants.all()