from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)  # ✅ Explicit use of CharField

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # ✅ Now handled via method

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data


# ✅ Example of using ValidationError for custom validation (if needed for message body)
class CreateMessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'message_body']

    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
