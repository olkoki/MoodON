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
        (0, 'Happiness level'),
        (1, 'Very unhappy'),
        (2, 'Unhappy'),
        (3, 'Neutral'),
        (4, 'Happy'),
        (5, 'Very happy'),
        (6, 'Over the moon'),
        (7, 'Ecstatic'),
    )
    ANGER_CHOICES = (
        (0, 'Anger level'),
        (1, 'Calm'),
        (2, 'Irritated'),
        (3, 'Annoyed'),
        (4, 'Frustrated'),
        (5, 'Angry'),
        (6, 'Fuming'),
        (7, 'Raging'),
    )
    ANXIETY_CHOICES = (
        (0, 'Anxiety level'),
        (1, 'Calm'),
        (2, 'Uneasy'),
        (3, 'Nervous'),
        (4, 'Anxious'),
        (5, 'Distressed'),
        (6, 'Terrified'),
        (7, 'Overwhelmed'),
    )
    ENERGY_CHOICES = (
        (0, 'Energy level'),
        (1, 'Exhausted'),
        (2, 'Tired'),
        (3, 'Neutral'),
        (4, 'Energetic'),
        (5, 'Excited'),
        (6, 'Hyperactive'),
        (7, 'Manic'),
    )
    MOTIVATION_CHOICES = (
        (0, 'Motivation level'),
        (1, 'Demotivated'),
        (2, 'Apathetic'),
        (3, 'Bored'),
        (4, 'Neutral'),
        (5, 'Motivated'),
        (6, 'Inspired'),
        (7, 'Obsessed'),
    )

    # Add fields for date, mood, anger, anxiety, energy, and motivation
    date = models.DateField()
    happiness = models.IntegerField(choices=HAPPINESS_CHOICES)
    anger = models.IntegerField(choices=ANGER_CHOICES)
    anxiety = models.IntegerField(choices=ANXIETY_CHOICES)
    energy = models.IntegerField(choices=ENERGY_CHOICES)
    motivation = models.IntegerField(choices=MOTIVATION_CHOICES)