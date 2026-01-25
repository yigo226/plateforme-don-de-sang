from datetime import date
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProfilDonneur(models.Model):

    GROUPE_SANGUIN = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil_donneur",
        verbose_name=_("Utilisateur")
    )

    date_naissance = models.DateField(
        verbose_name=_("Date de naissance")
    )

    poids = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Poids (kg)")
    )

    groupe_sanguin = models.CharField(
        max_length=3,
        choices=GROUPE_SANGUIN,
        blank=True,
        null=True,
        verbose_name=_("Groupe sanguin")
    )

    groupe_sanguin_verrouille = models.BooleanField(
        default=False,
        verbose_name=_("Groupe sanguin verrouillé")
    )

    est_eligible = models.BooleanField(
        default=True,
        verbose_name=_("Éligible au don")
    )

    date_dernier_don = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Date du dernier don")
    )

    remarques_medicales = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Remarques médicales")
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    def age(self):
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) <
            (self.date_naissance.month, self.date_naissance.day)
        )

    def clean(self):
        if self.age() < 18:
            raise ValidationError(_("Âge minimum requis : 18 ans"))

    def __str__(self):
        return f"Donneur : {self.utilisateur.username}"
