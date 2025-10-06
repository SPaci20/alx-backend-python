from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class UserMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Message.objects.filter(receiver=username)

class UnreadMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Message.objects.filter(receiver=username, is_read=False)