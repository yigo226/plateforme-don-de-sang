from django import forms
from .models import Utilisateur

class InscriptionDonneurForm(forms.ModelForm):
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation du mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['email','first_name','last_name','telephone','ville']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', "Les mots de passe ne correspondent pas")
        return cleaned_data
