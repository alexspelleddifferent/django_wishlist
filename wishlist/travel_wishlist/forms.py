from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    # defining a Place object to be used in the database and the websites
    class Meta:
        model = Place
        fields = ('name', 'visited')

# make a new date form
class DateInput(forms.DateInput):
    input_type = 'date'

# making a new form for review of a trip
class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        widgets = { 'date_visited': DateInput() }