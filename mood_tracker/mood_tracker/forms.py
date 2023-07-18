# mood_calendar/forms.py
from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Task, Medicine, MedsReminders

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

class ReminderCreateForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReminderUpdateForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'is_finished', 'is_notified']
        labels = {'is_finished':'Mark as Done'}
        widgets = {
            'due_date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MedicineForm(forms.ModelForm):
    
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'amount', 'dose', 'dose_time']

class MedsReminderForm(forms.ModelForm):
    class Meta:
        model = MedsReminders
        fields = ['time']

class MedsUpdateForm(forms.ModelForm):
        class Meta:
            model = Medicine
            fields = ['name', 'description', 'amount', 'dose', 'dose_time']
