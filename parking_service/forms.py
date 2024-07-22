from django import forms

from parking_service.models import Vehicle, LicensePlate

class LicensePlateForm(forms.ModelForm):
    plate_number = forms.CharField(
        min_length=3, max_length=10, required=True, widget=forms.TextInput()
    )
    image = forms.ImageField()

    class Meta:
        model = LicensePlate
        fields = ("image", 'plate_number')


class VehicleForm(forms.ModelForm):
    plate_number = forms.CharField(
        min_length=3, max_length=10, required=True, widget=forms.TextInput()
    )

    class Meta:
        model = Vehicle
        fields = ("plate_number",)
