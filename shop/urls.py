from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('my_cart/', views.my_cart, name='cart'),
    path('profile/<int:pk>/', views.customer_profile, name='customer_profile'),

    #cart
    # path('checkout/', views.Checkout.as_view(), name='checkout')
    path('checkout/', views.checkout, name='checkout'),
    path('create-checkout-session/', views.create_checkout_sessionn, name='create-checkout-session'),
    path("success/", views.success, name="success"),
    path("order_summary/", views.order_summary, name="order_summary"),
    path("cancel/", views.cancel, name="cancel"),
    # path('config/', views.stripe_config),  # new
]