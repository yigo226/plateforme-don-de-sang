from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
# class ProfilDonneur(models.Model):


class ProfilDonneur(models.Model):

    GROUPE_SANGUIN = [
        ('INCONNU', 'Inconnu'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    utilisateur = models.OneToOneField(
        'comptes.Utilisateur',
        on_delete=models.CASCADE,
        related_name='profil_donneur'
    )

    date_naissance = models.DateField()
    poids = models.PositiveIntegerField()

    groupe_sanguin = models.CharField(
        max_length=7,
        choices=GROUPE_SANGUIN,
        default='INCONNU'
    )
    groupe_sanguin_verrouille = models.BooleanField(default=False)
    nb_modifications_groupe = models.PositiveSmallIntegerField(default=0)

    def age(self):
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
        )
    
    date_dernier_don = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date du dernier don"
    )

    def clean(self):
        if self.age() < 18:
            raise ValidationError("Âge minimum requis : 18 ans.")

        if self.pk:
            ancien = ProfilDonneur.objects.get(pk=self.pk)

            if ancien.groupe_sanguin != self.groupe_sanguin:
                if ancien.groupe_sanguin_verrouille:
                    raise ValidationError("Groupe sanguin définitivement verrouillé.")

                if ancien.nb_modifications_groupe >= 1:
                    raise ValidationError(
                        "Vous avez déjà corrigé votre groupe sanguin. "
                        "Il est maintenant verrouillé."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk:
            ancien = ProfilDonneur.objects.get(pk=self.pk)

            if ancien.groupe_sanguin != self.groupe_sanguin:
                # première vraie saisie
                if ancien.groupe_sanguin == 'INCONNU':
                    self.nb_modifications_groupe = 0
                else:
                    # correction
                    self.nb_modifications_groupe += 1

                # après la correction → verrouillage
                if self.nb_modifications_groupe >= 1:
                    self.groupe_sanguin_verrouille = True

        super().save(*args, **kwargs)
# 
    def __str__(self):
        return f"{self.utilisateur.email} - Donneur"
