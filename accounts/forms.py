from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

class SignUpForm(UserCreationForm):
    """
        UserCreationForm -> username, pass1, pass2 has attritube
    """

    class Meta:
        model = User
        fields = ['username']