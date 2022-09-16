from django.shortcuts import render, redirect, reverse
from django.shortcuts import render
from . import views
from django.views import generic

from .forms import *

# Create your views here.
def home(request):
    
    return render(request, 'home.html')

def signup(request):
    return render(request, 'registration/signup.html')

def login(request):
    return render(request, 'registration/login.html')

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomerUserCreationForm

    def get_success_url(self):
        return reverse("shop:login")


    