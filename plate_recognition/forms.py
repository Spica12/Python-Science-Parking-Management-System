from django import forms

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

class ConfirmPlateForm(forms.Form):
    confirm_plate_number = forms.CharField(
        min_length=3, max_length=10, required=False, widget=forms.TextInput()
    )
