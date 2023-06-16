# project/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Other URL patterns for your project...
    path('admin/', admin.site.urls),
    path('', include('mood_calendar.urls')),
]