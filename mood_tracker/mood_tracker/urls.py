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
from .views import cal1, cal2, home

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.dashboard, name='home_page'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('account/', views.accountSettings, name='account'),
    path('calendar/<int:year>/<int:month>', cal1, name='calendar'),
    path('calendar/<int:year>/<int:month>/', cal1, name='calendar'),
    path('calendar/', cal2, name='calendar'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete/password_reset_complete.html'), name='password_reset_complete'),

    path("accounts/profile/", TemplateView.as_view(template_name='profile/profile.html'), name="profile"),
    
    path('relaxation/', TemplateView.as_view(template_name='relaxation/relaxation.html'), name='relaxation'),
    path('relaxation/breathing/', TemplateView.as_view(template_name='relaxation/breathing.html'), name='breathing'),
    path('relaxation/imagery/', TemplateView.as_view(template_name='relaxation/imagery.html'), name='imagery'),
    path('relaxation/muscle/', TemplateView.as_view(template_name='relaxation/muscle.html'), name='muscle'),
    
    #path('meds-tracking/', TemplateView.as_view(template_name='meds/meds.html'), name='meds'),
    path('meds-tracking/add_medicine/', views.MedicineCreate.as_view(), name='add_med'),
    path('meds-tracking/update/<int:pk>/', views.MedicineUpdate.as_view(), name='meds_update'),
    path('meds-tracking/delete/<int:pk>/', views.MedicineDelete.as_view(), name='meds_delete'),
    path('meds-tracking/mark-taken/<int:medicine_id>/', views.mark_taken, name='mark_taken'),
    path('meds-tracking/', views.info_meds, name='info_meds'),

    #path('to-do/', views.ReminderList.as_view(), name='info_tasks'),
    path('to-do/task/add/', views.ReminderCreate.as_view(), name='task_add'),
    path('to-do/task-update/<int:pk>/', views.ReminderUpdate.as_view(), name='task_update'),
    path('to-do/task/<int:pk>/delete/', views.ReminderDelete.as_view(), name='task_delete'),
    path('to-do/task/<int:pk>/finish/', views.finish_task, name='finish_task'),
    path('to-do/task/<int:pk>/unfinish/', views.unfinish_task, name='unfinish_task'),
    path('to-do/', views.info_tasks, name='info_tasks'),

    #path('daily-routine/', views.DailyRoutineList.as_view(), name='routine_list'),
    path('daily-routine/add/', views.DailyRoutineCreate.as_view(), name='routine_add'),
    path('daily-routine/update/<int:pk>/', views.DailyRoutineUpdate.as_view(), name='routine_update'),
    path('daily-routine/<int:pk>/delete/', views.DailyRoutineDelete.as_view(), name='routine_delete'),
    path('daily-routine/<int:pk>/finish/', views.mark_as_done, name='finish_routine'),
    path('daily-routine/<int:pk>/unfinish/', views.mark_undone, name='unfinish_routine'),
    path('daily-routine/', views.routine_list, name='routine_list'),

    path('psychoeducation/', TemplateView.as_view(template_name='edu/edu_main.html'), name='edu'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
