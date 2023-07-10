# mood_calendar/views.py
from django.shortcuts import render, redirect, HttpResponse
from .forms import MoodEntryForm, CreateUserForm, CustomerForm
from schedule.models import Event
from .models import MoodEntry, Profile, Mood
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users
import calendar
from datetime import datetime, date
from django.views import View
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from schedule.periods import Day
from django.views.generic import TemplateView
from django.template import loader
from django.contrib.auth.models import User
from django.template.defaulttags import register

import seaborn as sns
import pandas as pd
import io
import base64

## template filter for extracting dictionary key
## https://fedingo.com/how-to-lookup-dictionary-value-with-key-in-django-template/
@register.filter
def get_mood_color(data, mood_type):
    dictionary, day = data
    colors = {
        0: "#E6E6FA",
        1: "#b6e2dd",
        2: "#c8ddbb",
        3: "#e9e5af",
        4: "#fbdf9d",
        5: "#fbc99d",
        6: "#fbb39d",
        7: "#fba09d",
        }
    return colors[getattr(dictionary.get(day)[0], mood_type)]


## https://stackoverflow.com/questions/420703/how-to-add-multiple-arguments-to-my-custom-template-filter-in-a-django-template
@register.filter(name='one_more')
def one_more(_1, _2):
    return _1, _2

@register.filter
def get_description(data, day):
    return data.get(day)[0].description

@register.filter
def get_mood_name(data, mood_type):
    dictionary, day = data
    names = {
        0: 'None',
        1: 'Very low',
        2: 'Low',
        3: 'Moderate',
        4: 'Medium',
        5: 'High',
        6: 'Very high',
        7: 'Extreme',
        }
    return names[getattr(dictionary.get(day)[0], mood_type)]

def home(request):
    template = loader.get_template('homepage/home.html')
    return HttpResponse(template.render())

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

@login_required(login_url='login')
class ProfileView(TemplateView):
    template_name = 'profile/profile.html'
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        try:
            d = Day.objects.filter(user__id=self.request.user.id).latest('date')
            #e = Entry.objects.filter(day__id=d.id).order_by('-created')
            #context['latest_entryset'] = e
            context['latest_day'] = d
            context['latest_date'] = d.date
            context['latest_day_value'] = d.date.day
            return context
        except:
            return context
    
    def get_user_id(self):
        return self.request.user.id

    def get_username(self):
       return self.request.user.get_username()

    def get_name(self):
        u = self.request.user
        return u.get_full_name()

    def get_year(self):
        d = date.today()
        print(type(d))
        return d.year

    def get_month(self):
        d = date.today()
        return d.month
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    try:
        profile = request.user.profile
    except User.profile.RelatedObjectDoesNotExist:
        # If the user doesn't have a profile, create a new one
        profile = Profile(user=request.user)

    form = CustomerForm(instance=profile)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'account_settings/account_settings.html', context)

class CalendarView(TemplateView):
    template_name = 'mood_calendar/calendar.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # Get the current month and year
        #now = datetime.now()
        year = kwargs['year']
        month = kwargs['month']
        
        prev_month = month - 1
        prev_year = year
        if prev_month == 0:
            prev_month = 12
            prev_year = prev_year - 1
        
        next_month = month + 1
        next_year = year
        if next_month == 13:
            next_month = 1
            next_year = next_year + 1

        # Generate the calendar for the current month
        cal = calendar.monthcalendar(year, month)
        user = self.request.user

        context["calendar"] = cal
        
        context ["mood"] = Mood

        context ["prev_link"] = f"/calendar/{prev_year}/{prev_month}"
        context ["next_link"] = f"/calendar/{next_year}/{next_month}"
        context ["plot_month_happiness"] = plot_month(year, month, user, "happiness")
        context ["plot_month_anger"] = plot_month(year, month, user, "anger")
        context ["plot_month_anxiety"] = plot_month(year, month, user, "anxiety")
        context ["plot_month_energy"] = plot_month(year, month, user, "energy")
        context ["plot_month_motivation"] = plot_month(year, month, user, "motivation")

        
        # Get the logged-in user's mood entries for the current month
        mood_entries = Mood.objects.filter(user=user, date__year=year, date__month=month)
        
        # Create a dictionary to hold the mood entries for each day
        print(mood_entries)
        mood_entries_dict = {}
        for entry in mood_entries:
            day = entry.date.day
            if day not in mood_entries_dict:
                mood_entries_dict[day] = []

            mood_entries_dict[day].append(entry)

        context ["mood_entries_dict"] = mood_entries_dict
        
        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        date = request.POST['date']
        happiness = request.POST['happiness']
        anger = request.POST['anger']
        anxiety = request.POST['anxiety']
        energy = request.POST['energy']
        motivation = request.POST['motivation']
        description = request.POST['description']
        Mood.objects.create(user=user, date=date, happiness=happiness, anger=anger, anxiety=anxiety, energy=energy, motivation=motivation, description=description)
        print('Hi')
        return redirect(reverse_lazy('calendar', kwargs={'year': kwargs['year'], 'month': kwargs['month']}))
    print('Hello World')
    
def cal1(request, year, month):
    print("Good Morning")
    return CalendarView.as_view()(request=request, year=year, month=month)

def cal2(request):
    current_date = date.today()
    return CalendarView.as_view()(request=request, year=current_date.year, month=current_date.month)

def plot_month(year, month, user, mood_name):
    mood_entries = Mood.objects.filter(user=user, date__year=year, date__month=month)
    data = pd.DataFrame(mood_entries.values())
    print(data)
    plot = sns.lineplot(data=data, x="date", y=mood_name)
    print(plot)
    img = io.BytesIO()
    plot.figure.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot.figure.clf()
    return "data:image/png;base64, {}".format(base64.b64encode(img.getvalue()).decode('utf-8'))