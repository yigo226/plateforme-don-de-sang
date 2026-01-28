from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
import re


# permet de gérer la création des utilisateurs et superutilisateurs
class UtilisateurManager(BaseUserManager):
    """
    Manager pour Utilisateur qui utilise email comme identifiant
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L’email doit être fourni')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



# Modèle personnalisé pour les utilisateurs
class Utilisateur(AbstractUser):
    # On désactive le username natif
    username = None

    class Role(models.TextChoices):
        DEMANDEUR = 'DEMANDEUR', _('Demandeur')
        DONNEUR = 'DONNEUR', _('Donneur')
        HOPITAL = 'HOPITAL', _('Hôpital')
        ADMIN = 'ADMIN', _('Administrateur')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DEMANDEUR
    )

    # 👉 Username métier (nom + chiffre)
    identifiant = models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        verbose_name=_("Identifiant utilisateur")
    )

    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    ville = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(blank=True, null=True)
    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def age(self):
        if not self.date_naissance:
            return None
        today = date.today()
        return today.year - self.date_naissance.year - (
            (today.month, today.day) <
            (self.date_naissance.month, self.date_naissance.day)
        )

    def _generer_identifiant(self):
        base = re.sub(r'\s+', '', self.last_name.lower())
        utilisateurs = Utilisateur.objects.filter(identifiant__startswith=base)

        if not utilisateurs.exists():
            return f"{base}1"

        numeros = []
        for u in utilisateurs:
            suffixe = u.identifiant.replace(base, "")
            if suffixe.isdigit():
                numeros.append(int(suffixe))

        return f"{base}{max(numeros) + 1 if numeros else 1}"

    def save(self, *args, **kwargs):
        if not self.identifiant and self.last_name:
            self.identifiant = self._generer_identifiant()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

