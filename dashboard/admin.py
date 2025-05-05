from django.contrib import admin
from .models import SecurityEvent

@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'description', 'timestamp', 'user_ip', 'user_agent')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('description', 'user_ip', 'user_agent')
