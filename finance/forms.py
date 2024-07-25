from datetime import datetime
from django import forms
from django.utils import timezone

from finance.models import Tariff


class TariffForm(forms.ModelForm):

    class Meta:
        model = Tariff
        fields = ['description', 'price_per_hour', 'start_date']
        widgets = {
            'description': forms.TextInput(),
            'price_per_hour': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        end_date_default = "2999-12-31"
        start_date_initial = "2024-01-01"
        self.initial["start_date"] = datetime.strptime(start_date_initial, "%Y-%m-%d")
        self.initial["end_date"] = datetime.strptime(end_date_default, "%Y-%m-%d")
        latest_object = self.Meta.model.objects.all().order_by("-start_date").first()
        if latest_object:
            min_date = latest_object.start_date + timezone.timedelta(days=1)
        else:
            min_date = timezone.now()
        self.initial["start_date"] = min_date.strftime("%Y-%m-%d")
        self.fields["start_date"].widget.attrs["min"] = min_date.strftime("%Y-%m-%d")
        self.fields["start_date"].widget.attrs["title"] = f'Minimum : {min_date.strftime("%Y-%m-%d")}'
