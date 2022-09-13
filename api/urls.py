from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('home', views.home, name='home')
]