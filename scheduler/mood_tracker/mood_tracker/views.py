# mood_calendar/views.py
from django.shortcuts import render, redirect
from .forms import MoodEntryForm, CreateUserForm
from schedule.models import Event
from .models import MoodEntry, Profile, Mood
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users
import calendar
from datetime import datetime
from django.views import View
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from schedule.periods import Day
from django.views.generic import TemplateView
from django.http import HttpRequest


@unauthenticated_user
def registerPage(request):    
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Profile.objects.create(
                user=user
            )

            messages.success(request, 'Account was created for ' + username)


            return redirect('login')
    
    context = {'form':form}
    return render(request, 'register/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')
            
    context = {}
    return render(request, 'login/login.html', context)
@login_required
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def mood_calendar(request):
    user = request.user

    # Get the current month and year
    now = datetime.now()
    year = now.year
    month = now.month

    # Generate the calendar for the current month
    cal = calendar.monthcalendar(year, month)

    # Get the logged-in user's mood entries for the current month
    mood_entries = MoodEntry.objects.filter(user=user, event__start__year=year, event__start__month=month)

    # Create a dictionary to hold the mood entries for each day
    mood_entries_dict = {}
    for entry in mood_entries:
        day = entry.event.start.day
        if day not in mood_entries_dict:
            mood_entries_dict[day] = []

        mood_entries_dict[day].append(entry)

    context = {
        'year': year,
        'month': month,
        'cal': cal,
        'mood_entries_dict': mood_entries_dict,
    }
    print(context)
    return render(request, 'mood_calendar/calendar.html', context)

@login_required
def add_mood_entry(request, event_id):
    event = Event.objects.get(pk=event_id)

    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.event = event
            mood_entry.save()
            return redirect('mood_calendar')
    else:
        form = MoodEntryForm()

    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'mood_calendar/add_mood_entry.html', context)

class CalendarView(TemplateView):
    template_name = 'mood_calendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current month and year
        now = datetime.now()
        year = now.year
        month = now.month

        # Generate the calendar for the current month
        cal = calendar.monthcalendar(year, month)
        context["calendar"] = cal
        
        context ["mood"] = Mood
        return context

    
    
    def post(self, request, *args, **kwargs):
        date = request.POST['date']
        happiness = request.POST['happiness']
        anger = request.POST['anger']
        anxiety = request.POST['anxiety']
        energy = request.POST['energy']
        motivation = request.POST['motivation']
        Mood.objects.create(date=date, happiness=happiness, anger=anger, anxiety=anxiety, energy=energy, motivation=motivation)
        print('Hi')
        return redirect(reverse_lazy('calendar', kwargs={'year': kwargs['year'], 'month': kwargs['month']}))
        
    print('Hello World')
def cal1(request, year, month):
    print("Good Morning")
    return CalendarView.as_view()(request=request, year=year, month=month)
