from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='')
    username = forms.CharField(max_length=150, required=True, help_text='')
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='')
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        help_texts = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
