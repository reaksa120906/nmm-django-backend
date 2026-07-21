from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf import settings as django_settings
from api.dashboard_views import dashboard, reports, savings_view, notifications, settings_view, profile_view
from api.flutter_view import serve_flutter

urlpatterns = [
    path('django-admin/',  admin.site.urls),
    path('admin/',         RedirectView.as_view(url='/dashboard/', permanent=False)),

    path('api/',           include('api.urls')),
    path('dashboard/',     dashboard,       name='dashboard'),
    path('reports/',       reports,         name='reports'),
    path('savings/',       savings_view,    name='savings'),
    path('notifications/', notifications,   name='notifications'),
    path('settings/',      settings_view,   name='settings'),
    path('profile/',       profile_view,    name='profile'),

    # Flutter web app — serves index.html for all unmatched routes
    path('app/',           serve_flutter,   name='flutter_index'),
    re_path(r'^app/.*$',   serve_flutter,   name='flutter_routes'),
]
