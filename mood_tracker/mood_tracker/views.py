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

## template filter for extracting dictionary key
## https://fedingo.com/how-to-lookup-dictionary-value-with-key-in-django-template/
@register.filter
def get_mood_color(data, mood_type):
    dictionary, day = data
    colors = {
        0: "blue",
        1: "black",
        2: "gray",
        3: "yellow",
        4: "orange",
        5: "red",
        6: "violet",
        7: "purple"}
    return colors[getattr(dictionary.get(day)[0], mood_type)]

## https://stackoverflow.com/questions/420703/how-to-add-multiple-arguments-to-my-custom-template-filter-in-a-django-template
@register.filter(name='one_more')
def one_more(_1, _2):
    return _1, _2

@register.filter
def get_description(data, day):
    return data.get(day)[0].description


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
        #now = datetime.now()
        year = kwargs['year']
        month = kwargs['month']
        # Generate the calendar for the current month
        cal = calendar.monthcalendar(year, month)
        context["calendar"] = cal
        
        context ["mood"] = Mood

        
        user = self.request.user

        # Get the logged-in user's mood entries for the current month
        mood_entries = Mood.objects.all()#.filter(user=user, event__start__year=year, event__start__month=month)
        
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
