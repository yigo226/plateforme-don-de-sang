from django import forms
from .models import ProfilDonneur

class ProfilDonneurForm(forms.ModelForm):
    class Meta:
        model = ProfilDonneur
        fields = ['date_naissance', 'poids', 'groupe_sanguin']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si le groupe sanguin est verrouillé, on désactive le champ
        if self.instance and self.instance.groupe_sanguin_verrouille:
            self.fields['groupe_sanguin'].disabled = True


from django import forms
from .models import ProfilDonneur

class ProfilDonneurUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfilDonneur
        fields = ['poids', 'groupe_sanguin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.groupe_sanguin_verrouille:
            self.fields['groupe_sanguin'].disabled = True

    def clean_groupe_sanguin(self):
        # Si verrouillé, renvoyer la valeur existante et empêcher modification
        groupe_actuel = self.instance.groupe_sanguin
        if self.instance.groupe_sanguin_verrouille:
            return groupe_actuel
        return self.cleaned_data['groupe_sanguin']