from temple.models import God
from django import forms

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
            'name': ('Imię'),
            'god_description': ('Opis'),
            'blessing_name': ('Nazwa błogosławieństwa'),
            'blessing_description': ('Opis błogosławieństwa'),
            'profile_pic': ('Wizerunek'),
        }
