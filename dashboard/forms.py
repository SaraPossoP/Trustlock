from django import forms
from .models import SecurityEvent

class SecurityEventForm(forms.ModelForm):
    class Meta:
        model = SecurityEvent
        exclude = ['user', 'user_ip', 'user_agent']
        widgets = {
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
