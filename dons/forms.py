from django import forms
from .models import Don
from hopitaux.models import Hopital

class DeclarationDonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = ['hopital']


class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = ['donneur', 'volume_ml']


class ValidationDonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = ['volume_ml']

    def clean_volume_ml(self):
        volume = self.cleaned_data['volume_ml']
        if volume < 300 or volume > 600:
            raise forms.ValidationError(
                "Le volume doit être compris entre 300 et 600 ml."
            )
        return volume
