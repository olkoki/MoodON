from __future__ import unicode_literals
from typing import Iterable, Optional

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import timedelta

import redis

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.urls import reverse
from six import python_2_unicode_compatible

import arrow

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    profile_picture = models.ImageField(default='profile2.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username

class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    HAPPINESS_CHOICES = (
        (0, 'Happiness'),
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'Medium'),
        (5, 'High'),
        (6, 'Very high'),
        (7, 'Extreme'),
    )
    ANGER_CHOICES = (
        (0, 'Anger'),
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'Medium'),
        (5, 'High'),
        (6, 'Very high'),
        (7, 'Extreme'),
    )
    ANXIETY_CHOICES = (
        (0, 'Anxiety'),
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'Medium'),
        (5, 'High'),
        (6, 'Very high'),
        (7, 'Extreme'),
    )
    ENERGY_CHOICES = (
        (0, 'Energy'),
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'Medium'),
        (5, 'High'),
        (6, 'Very high'),
        (7, 'Extreme'),
    )
    MOTIVATION_CHOICES = (
        (0, 'Motivation'),
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'Medium'),
        (5, 'High'),
        (6, 'Very high'),
        (7, 'Extreme'),
    )

    # Add fields for date, mood, anger, anxiety, energy, and motivation
    date = models.DateField()
    happiness = models.IntegerField(choices=HAPPINESS_CHOICES)
    anger = models.IntegerField(choices=ANGER_CHOICES)
    anxiety = models.IntegerField(choices=ANXIETY_CHOICES)
    energy = models.IntegerField(choices=ENERGY_CHOICES)
    motivation = models.IntegerField(choices=MOTIVATION_CHOICES)
    description = models.CharField(max_length=200, default='Hello world')

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('due_date',)
    
    def __str__(self):
        return self.title
    
    def has_alarm(self):
        return self.due_date is not None
    
    def has_expired(self):
        if self.has_alarm():
            return timezone.now() > self.due_date
        else:
            return False
        
    def status(self):
        if self.is_finished:
            return 'is_finished'
        elif self.has_expired():
            return 'Expired'
        else:
            return "In progress"

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)
    dose = models.PositiveIntegerField(default=1)
    reminders = models.ManyToManyField('MedsReminders')
    
    def __str__(self):
        return self.name
    
    def minus_dose(self):
        if self.amount >= self.dose:
            self.amount -= self.dose
            self.save()
        
class MedsReminders(models.Model):
    name = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    time = models.TimeField()

    def __str__(self):
        return f"{self.medicine.name} - {self.time}"
    
#https://stackoverflow.com/questions/72264677/how-can-i-implement-notifications-system-in-django
class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    time = models.TimeField()

class DailyRoutine(models.Model):
    title = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)