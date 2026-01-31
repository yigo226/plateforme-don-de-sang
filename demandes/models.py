from django.db import models

# Create your models here.

from django.db import models
from django.core.exceptions import ValidationError

from comptes.models import Utilisateur
from hopitaux.models import Hopital
from donneurs.models import ProfilDonneur


class DemandeSang(models.Model):

    class Statut(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        SATISFAITE = 'SATISFAITE', 'Satisfaite'
        REFUSEE = 'REFUSEE', 'Refusée'
        EXPIREE = 'EXPIREE', 'Expirée'

    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='demandes'
    )

    ville = models.CharField(max_length=100)

    hopital = models.ForeignKey(
        Hopital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demandes'
    )

    hopital_autre = models.CharField(
        max_length=255,
        blank=True
    )

    groupe_sanguin = models.CharField(
        max_length=7,
        choices=ProfilDonneur.GROUPE_SANGUIN
    )

    # Volume
    volume_ml = models.PositiveIntegerField(
        default=450,
        help_text="450 ml par défaut pour un patient"
    )

    motif = models.TextField(blank=True)

    contact = models.CharField(
        max_length=50
    )

    statut = models.CharField(
        max_length=15,
        choices=Statut.choices,
        default=Statut.ACTIVE
    )

    date_demande = models.DateTimeField(auto_now_add=True)


    def clean(self):

        # 🔐 Sécurité : auteur pas encore injecté
        if not self.auteur_id:
            return

        est_hopital = self.auteur.role == Utilisateur.Role.HOPITAL

        # 🏥 CAS HÔPITAL
        if est_hopital:
            if not self.volume_ml or self.volume_ml < 300:
                raise ValidationError(
                    "Un hôpital doit préciser un volume de sang valide (≥ 300 ml)."
                )
            return

        # 👤 CAS NON HÔPITAL (demandeur / donneur)
        self.volume_ml = 450

        if not self.hopital and not self.hopital_autre:
            raise ValidationError(
                "Veuillez indiquer l’hôpital ou sa localisation."
            )

    def __str__(self):
        return f"{self.groupe_sanguin} - {self.volume_ml}ml ({self.ville})"

# demandes/models.py
class ReponseDonneur(models.Model):
    demande = models.ForeignKey(DemandeSang, on_delete=models.CASCADE)
    donneur = models.ForeignKey(ProfilDonneur, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    date_reponse = models.DateTimeField(auto_now_add=True)
    accepte = models.BooleanField(default=False)
