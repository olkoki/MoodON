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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50)

class Mood(models.Model):
    HAPPINESS_CHOICES = (
        (1, 'Very unhappy'),
        (2, 'Unhappy'),
        (3, 'Slightly unhappy'),
        (4, 'Neutral'),
        (5, 'Slightly happy'),
        (6, 'Happy'),
        (7, 'Very happy'),
        (8, 'Extremely happy'),
        (9, 'Over the moon'),
        (10, 'Ecstatic'),
    )
    ANGER_CHOICES = (
        (1, 'Calm'),
        (2, 'Irritated'),
        (3, 'Annoyed'),
        (4, 'Frustrated'),
        (5, 'Angry'),
        (6, 'Enraged'),
        (7, 'Fuming'),
        (8, 'Livid'),
        (9, 'Seething'),
        (10, 'Raging'),
    )
    ANXIETY_CHOICES = (
        (1, 'Calm'),
        (2, 'Uneasy'),
        (3, 'Nervous'),
        (4, 'Apprehensive'),
        (5, 'Anxious'),
        (6, 'Panicky'),
        (7, 'Distressed'),
        (8, 'Terrified'),
        (9, 'Paralyzed'),
        (10, 'Overwhelmed'),
    )
    ENERGY_CHOICES = (
        (1, 'Exhausted'),
        (2, 'Sleepy'),
        (3, 'Tired'),
        (4, 'Fatigued'),
        (5, 'Neutral'),
        (6, 'Energetic'),
        (7, 'Excited'),
        (8, 'Hyperactive'),
        (9, 'Manic'),
        (10, 'Unstoppable'),
    )
    MOTIVATION_CHOICES = (
        (1, 'Demotivated'),
        (2, 'Apathetic'),
        (3, 'Uninterested'),
        (4, 'Bored'),
        (5, 'Neutral'),
        (6, 'Interested'),
        (7, 'Motivated'),
        (8, 'Inspired'),
        (9, 'Passionate'),
        (10, 'Obsessed'),
    )

    # Add fields for date, mood, anger, anxiety, energy, and motivation
    date = models.DateField()
    happiness = models.IntegerField(choices=HAPPINESS_CHOICES)
    anger = models.IntegerField(choices=ANGER_CHOICES)
    anxiety = models.IntegerField(choices=ANXIETY_CHOICES)
    energy = models.IntegerField(choices=ENERGY_CHOICES)
    motivation = models.IntegerField(choices=MOTIVATION_CHOICES)