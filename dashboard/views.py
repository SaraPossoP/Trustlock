from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime
from .models import SecurityEvent
from .forms import SecurityEventForm
import json
import csv
from django.http import HttpResponse
from . import views




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard_stats')
        else:
            return render(request, 'dashboard/login.html', {'error': 'Invalid credentials'})
    return render(request, 'dashboard/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'dashboard/logout.html')

@login_required
def dashboard_stats(request):
    
    if request.user.is_superuser:
        events = SecurityEvent.objects.all()
    else:
        events = SecurityEvent.objects.filter(user=request.user)

    labels = []
    data = []
    recent_events = []
    total_events = 0

    if events.exists():
        event_data = events.values('event_type').annotate(total=Count('event_type'))
        labels = [e['event_type'] for e in event_data]
        data = [e['total'] for e in event_data]
        recent_events = events.order_by('-timestamp')[:5]
        total_events = events.count()

    return render(request, 'dashboard/dashboard_stats.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'total_events': total_events,
        'recent_events': recent_events,
    })


@login_required
def create_event(request):
    if request.method == 'POST':
        form = SecurityEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            event.user_ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            event.user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
            
            event.save()


            if event.event_type in ['login_failed', 'suspicious_transfer', 'account_usage', 'location_change']:
                messages.warning(
                    request,
                    f"⚠️ ALERT: A critical event was detected.: {event.get_event_type_display()}"
                )

            messages.success(request, "Event successfully created.")
            return redirect('event_list')
    else:
        form = SecurityEventForm()

    return render(request, 'dashboard/create_event.html', {'form': form})


@login_required
def event_list(request):
    query = request.GET.get('q', '')
    event_type = request.GET.get('event_type', '')
    start_date = datetime.strptime(request.GET.get('start_date', ''), '%Y-%m-%d') if request.GET.get('start_date') else None
    end_date = datetime.strptime(request.GET.get('end_date', ''), '%Y-%m-%d') if request.GET.get('end_date') else None

    if request.user.is_superuser:
        events = SecurityEvent.objects.all().order_by('-timestamp')
    else:
        events = SecurityEvent.objects.filter(user=request.user).order_by('-timestamp')

    if query:
        search_filter = Q(event_type__icontains=query) | Q(description__icontains=query)
        if request.user.is_superuser:
            search_filter |= Q(user__username__icontains=query)
        events = events.filter(search_filter)

    if event_type:
        events = events.filter(event_type=event_type)
    if start_date:
        events = events.filter(timestamp__date__gte=start_date)
    if end_date:
        events = events.filter(timestamp__date__lte=end_date)

    event_types = events.values_list('event_type', flat=True).distinct()

    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/event_list.html', {
        'page_obj': page_obj,
        'query': query,
        'event_types': event_types,
        'selected_type': event_type,
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
    })



@login_required
def export_events_csv(request):
    query = request.GET.get('q', '')
    event_type = request.GET.get('event_type', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if request.user.is_superuser:
        events = SecurityEvent.objects.all()
    else:
        events = SecurityEvent.objects.filter(user=request.user)

    if query:
        search_filter = Q(event_type__icontains=query) | Q(description__icontains=query)
        if request.user.is_superuser:
            search_filter |= Q(user__username__icontains=query)
        events = events.filter(search_filter)

    if event_type:
        events = events.filter(event_type=event_type)
    if start_date:
        events = events.filter(timestamp__date__gte=start_date)
    if end_date:
        events = events.filter(timestamp__date__lte=end_date)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="security_events.csv"'

    writer = csv.writer(response)
    
    if request.user.is_superuser:
        writer.writerow(['ID', 'User', 'Type', 'Description', 'Timestamp'])
    else:
        writer.writerow(['ID', 'Type', 'Description', 'Timestamp'])

    for event in events:
        if request.user.is_superuser:
            writer.writerow([event.id, event.user.username, event.event_type, event.description, event.timestamp])
        else:
            writer.writerow([event.id, event.event_type, event.description, event.timestamp])

    return response