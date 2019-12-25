from django.contrib.auth.models import User
from subscribe.models import UserProfileInfo
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.db import models



# Set the regular user form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło', help_text='Minimum 8 znaków')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'password2')
        labels = {
            'username': ('Nazwa użytkownika'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError(
                'Ten mail jest już zajęty'
            )

        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        print(password)
        print(password2)
        print(self.cleaned_data)

        if password != password2:
            raise forms.ValidationError("Wpisane hasła nie są takie same.")
        else:
            validate_password(password)

        return password


# Set additional profile information class
class UserProfileForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = (
            'profile_pic',
        )
        labels = {
            'profile_pic': ('Zdjęcie profilowe'),
        }


# Allow users to update their profile picture
class UserProfileUpdate(forms.ModelForm):

    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')

    class Meta:
        model = UserProfileInfo
        fields = (
            'profile_pic',
        )


# Allow users to update their user data
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )