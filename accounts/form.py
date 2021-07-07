from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class Register_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class Profile_form(ModelForm):
    class Meta:
        model = Profile
        fields = ['Address']

class Login_form(forms.Form):
    Email = forms.EmailField()
    Password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class Edit_form(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','email']
