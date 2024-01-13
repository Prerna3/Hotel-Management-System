from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms.widgets import TextInput, PasswordInput


class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username","email","password1","password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control'}))