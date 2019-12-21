from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from subscribe.models import UserProfileInfo


# Set the regular user form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')
    password_repeat = forms.CharField(widget=forms.PasswordInput(), label='Powtórz hasło')

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'password_repeat')
        labels = {
            'username': ('Nazwa użytkownika'),
        }


# Set additional profile information class
class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)
        labels = {
            'profile_pic': ('Zdjęcie profilowe'),
        }