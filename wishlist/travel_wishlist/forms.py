from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    # defining a Place object to be used in the database and the websites
    class Meta:
        model = Place
        fields = ('name', 'visited')