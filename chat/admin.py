from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'is_private')
    list_filter = ('is_private', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username') 