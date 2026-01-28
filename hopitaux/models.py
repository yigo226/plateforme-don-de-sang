from django.db import models
from comptes.models import Utilisateur
# Create your models here.

class Hopital(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='hopital'
    )

    nom = models.CharField(max_length=150)
    ville = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField(blank=True)

    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
