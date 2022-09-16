from django.urls import path
from . import views
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', views.login, name='login'),


]