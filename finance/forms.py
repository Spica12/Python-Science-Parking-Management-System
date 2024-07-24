from datetime import datetime
from django import forms
from django.utils import timezone

from finance.models import Tariff


class TariffForm(forms.ModelForm):

    class Meta:
        model = Tariff
        fields = ['price_per_hour', 'start_date', 'end_date']
        widgets = {
            'price_per_hour': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        end_date_default = "2999-12-31 23:59"
        self.initial["end_date"] = datetime.strptime(end_date_default, "%Y-%m-%d %H:%M")
        latest_object = self.Meta.model.objects.all().order_by("-start_date").first()
        if latest_object:
            min_date = latest_object.start_date
            min_date += timezone.timedelta(minutes=1)
            self.fields["start_date"].widget.attrs["min"] = min_date.strftime(
                "%Y-%m-%dT%H:%M"
            )
            self.fields["start_date"].widget.attrs[
                "title"
            ] = f'Minimum : {min_date.strftime("%Y-%m-%d %H:%M")}'

    def clean_end_date(self):
        end_date: datetime = self.cleaned_data.get("end_date")
        if end_date and end_date.minute == 59:
            end_date = end_date.replace(second=59)
        return end_date
