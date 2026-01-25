from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Utilisateur(AbstractUser):

    email = models.EmailField(
        unique=True,
        verbose_name=_("Adresse email")
    )

    telephone = models.CharField(
        max_length=20,
        verbose_name=_("Téléphone")
    )

    ville = models.CharField(
        max_length=100,
        verbose_name=_("Ville")
    )

    est_patient = models.BooleanField(
        default=False,
        verbose_name=_("Est patient")
    )

    est_donneur = models.BooleanField(
        default=False,
        verbose_name=_("Est donneur")
    )

    recevoir_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Recevoir des notifications")
    )

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
