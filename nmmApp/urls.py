from django.urls import path, include, re_path
from django.views.generic import RedirectView
from api.dashboard_views import (
    dashboard, reports, savings_view, notifications,
    settings_view, profile_view, login_view, logout_view,
)
from api.flutter_view import serve_flutter

urlpatterns = [
    # /django-admin/ is hidden — redirect to custom dashboard
    path('django-admin/',      RedirectView.as_view(url='/dashboard/', permanent=False)),

    # Custom auth
    path('login/',             login_view,      name='login'),
    path('logout/',            logout_view,     name='logout'),

    path('admin/',             RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('api/',               include('api.urls')),

    # Custom admin dashboard
    path('dashboard/',         dashboard,       name='dashboard'),
    path('reports/',           reports,         name='reports'),
    path('savings/',           savings_view,    name='savings'),
    path('notifications/',     notifications,   name='notifications'),
    path('settings/',          settings_view,   name='settings'),
    path('profile/',           profile_view,    name='profile'),

    # Root → dashboard
    path('',                   RedirectView.as_view(url='/dashboard/', permanent=False)),

    # Flutter web app — serves index.html for all unmatched routes
    path('app/',               serve_flutter,   name='flutter_index'),
    re_path(r'^app/.*$',       serve_flutter,   name='flutter_routes'),
]
