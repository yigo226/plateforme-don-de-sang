from .models import ProfilDonneur
from django.core.exceptions import ValidationError


def devenir_donneur(utilisateur, date_naissance, poids):
    if utilisateur.role == utilisateur.Role.DONNEUR:
        raise ValidationError("Utilisateur déjà donneur")

    profil = ProfilDonneur.objects.create(
        utilisateur=utilisateur,
        date_naissance=date_naissance,
        poids=poids
    )

    utilisateur.role = utilisateur.Role.DONNEUR
    utilisateur.save()

    return profil
