from django import forms
from . import models

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='First name ', required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name ', required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username ', required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email ', required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'email'}))
    password = forms.CharField(label='Password ', required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    confirm_password = forms.CharField(label='Confirm password ', required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))


    class Meta:
        model = models.User
        fields = []

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Username ', required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password ', required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))



    class Meta:
        model = models.User
        fields = []