from django import forms
from django.contrib.auth.models import User
from subscribe.models import UserProfileInfo


# Set the regular user form
class UserForm(forms.ModelForm):
    # Additional field added to the form
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')


# Set additional profile information class
class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)