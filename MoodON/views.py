from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django.template.loader import get_template
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm


def home(request):
    template = loader.get_template('homepage/home.html')
    return HttpResponse(template.render())

#def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register/register.html', {'form': form})

def login(request):
    template = loader.get_template('login/login.html')
    return HttpResponse(template.render())
