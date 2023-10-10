from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'id', 'password']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'password']