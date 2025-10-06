from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'subject', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read')
    search_fields = ('sender', 'receiver', 'subject', 'body')