from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import timedelta
from schedule.models import Event

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    profile_picture = models.ImageField(default='profile2.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username



class MoodEntry(models.Model):
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50)

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