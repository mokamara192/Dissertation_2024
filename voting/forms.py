from django import forms
from .models import Candidate, VotingSession, VoteUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True, max_length=30)
    message = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        fields = ['name', 'email', 'message']


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__' 

# This for displays the list of voters that paticipated in the voting process
class VotedForm(forms.ModelForm):
    class Meta:
        model = VoteUser
        fields = ['user', 'voting_session'] 



class PositionForm(forms.ModelForm):
    class Meta:
        model = VotingSession
        fields = ['name', 'year', 'university', 'image', 'candidates', 'active']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']
    

    