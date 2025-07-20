from django.contrib import admin
from .models import USer, Conversation, Message

# Register your models here.
admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Message)
