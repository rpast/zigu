from temple.models import God
from django import forms
from django.db import models

# Create a God form
class GodForm(forms.ModelForm):
    class Meta():
        model = God
        fields = (
            'name',
            'god_description',
            'blessing_name',
            'blessing_description',
            'profile_pic',
        )
        labels = {
            'name': ('Imię bóstwa'),
            'god_description': ('Opis bóstwa'),
            'blessing_name': ('Nazwa błogosławieństwa'),
            'blessing_description': ('Opis błogosławieństwa'),
            'profile_pic': ('Wizerunek'),
        }
