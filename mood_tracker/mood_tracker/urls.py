"""mood_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from .views import cal1, home


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home_page'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('account/', views.accountSettings, name='account'),
    #path('mood-calendar/', views.mood_calendar, name='mood_calendar'),
    #path('mood-calendar/add/<int:event_id>/', views.add_mood_entry, name='add_mood_entry'),
    path('calendar/<int:year>/<int:month>/', cal1, name='calendar'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete/password_reset_complete.html'), name='password_reset_complete'),

    path("accounts/profile/", TemplateView.as_view(template_name='profile/profile.html'), name="profile"),
]
