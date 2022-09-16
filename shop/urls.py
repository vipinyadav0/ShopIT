from django.urls import path
from . import views
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('my_cart/', views.my_cart, name='cart'),

    


]