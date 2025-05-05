from django.db import models
from django.contrib.auth.models import User 

class SecurityEvent(models.Model):
    EVENT_TYPES = [
        ('login_failed', 'Login Failed'),
        ('suspicious_transfer', 'Suspicious Transfer'),
        ('location_change', 'Location Change'),
        ('account_usage', 'Unusual Account Usage'),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.event_type} at {self.timestamp}"
