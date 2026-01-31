from django.db import models

# Create your models here.
from django.db import models
from comptes.models import Utilisateur
from demandes.models import DemandeSang
from donneurs.models import ProfilDonneur

class Notification(models.Model):

    class Type(models.TextChoices):
        DEMANDE_SANG = 'DEMANDE_SANG', 'Demande de sang'
        REPONSE_DONNEUR = 'REPONSE_DONNEUR', 'Réponse donneur'

    destinataire = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    type = models.CharField(
        max_length=30,
        choices=Type.choices
    )

    message = models.TextField()

    lien = models.CharField(max_length=255, blank=True)

    lu = models.BooleanField(default=False)

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} → {self.destinataire}"


