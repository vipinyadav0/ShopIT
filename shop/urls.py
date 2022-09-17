from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('my_cart/', views.my_cart, name='cart'),
    path('profile/<int:pk>/', views.customer_profile, name='customer_profile'),

    #cart
    path('add-to-cart/<int:pk>', views.add_to_cart,name='add-to-cart'),




    


]