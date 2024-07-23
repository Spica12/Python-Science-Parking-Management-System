from django import forms

from parking_service.models import Vehicle, LicensePlate

# class LicensePlateForm(forms.ModelForm):
#     plate_number = forms.CharField(
#         min_length=3, max_length=10, required=True, widget=forms.TextInput()
#     )
#     image = forms.ImageField(
#         widget=forms.FileInput(
#             attrs={
#                 "title": "Upload photo of car",
#             }
#         )
#     )


class UploadFileForm(forms.Form):
    manual_plate_number = forms.CharField(
        min_length=3, max_length=10, required=False, widget=forms.TextInput()
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "title": "Upload photo of car",
            }
        )
    )


class VehicleForm(forms.ModelForm):
    plate_number = forms.CharField(
        min_length=3, max_length=10, required=True, widget=forms.TextInput()
    )

    class Meta:
        model = Vehicle
        fields = ("plate_number",)
