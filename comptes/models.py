from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Utilisateur(AbstractUser):

    class Role(models.TextChoices):
        DONNEUR = 'DONNEUR', 'Donneur'
        HOPITAL = 'HOPITAL', 'Hôpital'
        ADMIN = 'ADMIN', 'Administrateur'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DONNEUR
    )
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    ville = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  
    
    def __str__(self):
        return self.email
