from django import forms
from .models import Utilisateur
from django.core.exceptions import ValidationError
from datetime import date


class InscriptionForm(forms.ModelForm):
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation du mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = [
            'email',
            'first_name',
            'last_name',
            'date_naissance',
            'telephone',
            'ville'
        ]

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', "Les mots de passe ne correspondent pas")

        date_naissance = cleaned_data.get('date_naissance')
        if date_naissance:
            age = date.today().year - date_naissance.year
            if age < 14:
                raise ValidationError("Âge minimum requis : 14 ans")

        return cleaned_data

    def save(self, commit=True):
        utilisateur = super().save(commit=False)
        utilisateur.role = Utilisateur.Role.DEMANDEUR
        utilisateur.set_password(self.cleaned_data['password1'])

        if commit:
            utilisateur.save()
        return utilisateur


# Profil utilisateur 
class ProfilUtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'date_naissance', 'telephone', 'ville']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }