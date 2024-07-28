from django import forms

class AddParkingSpotsForm(forms.Form):
    number_of_spots = forms.IntegerField(min_value=1, max_value=9999, label="Number of Parking Spots")
