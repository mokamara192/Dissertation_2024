from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    id_number = forms.CharField(label='IDC Number', widget=forms.TextInput(attrs={'placeholder': 'Enter IDC number...'}))
    issued_by = forms.CharField(label='IDC Issuer', widget=forms.TextInput(attrs={'placeholder': 'Enter IDC issuer...'}))
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'placeholder': '1 Main Silicon hills'}))
    city = forms.CharField()
  

    class Meta:
        model = Profile
        fields = ['image', 'id_number', 'issued_by', 'address', 'city']

