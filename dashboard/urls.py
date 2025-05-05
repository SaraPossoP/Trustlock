from django.urls import path
from . import views
from .views import create_event

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('stats/', views.dashboard_stats, name='dashboard_stats'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('create/', create_event, name='create_event'),
    path('export-csv/', views.export_events_csv, name='export_events_csv'),


]
