from django.shortcuts import render, redirect, reverse
from django.shortcuts import render
from . import views
from django.views import generic
from .models import Product
from django.contrib.auth.views import LoginView, LogoutView

from .forms import *

# Create your views here.
def home(request):
    query = Product.objects.all()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'products': query,
        'num_visits' : num_visits
    }
    return render(request, 'home.html', context)

def signup(request):
    return render(request, 'registration/signup.html')

def login(request):
    return render(request, 'registration/login.html')

def my_cart(request):
    return render(request, 'cart.html')

# class LoginView(generic.DetailView):
#     template_name = "registration/login.html"
#     form_class = CustomerLoginForm


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomerUserCreationForm

    def get_success_url(self):
        return reverse("login")
    
class LogoutViewRedirect(LogoutView):
    template_name = "registration/logout.html"

    def get_success_url(self):
        return reverse('shop:home')    


    