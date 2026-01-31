from django import forms
from .models import DemandeSang
from comptes.models import Utilisateur


class DemandeSangForm(forms.ModelForm):
    class Meta:
        model = DemandeSang
        fields = [
            'ville',
            'hopital',
            'hopital_autre',
            'groupe_sanguin',
            'volume_ml',
            'motif',
            'contact',
        ]
        widgets = {
            'motif': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # sécurité absolue
        if not user:
            self.fields.pop('volume_ml', None)
            return

        # Cas non hôpital
        if user.role != Utilisateur.Role.HOPITAL:
            self.fields.pop('volume_ml', None)

        # 🏥 Cas hôpital
        else:
            self.fields.pop('hopital', None)
            self.fields.pop('hopital_autre', None)