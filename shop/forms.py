import email
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.CharField(max_length=10)

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        
