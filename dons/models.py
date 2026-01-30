from django.db import models

# Create your models here.
from django.db import models
from donneurs.models import ProfilDonneur
from hopitaux.models import Hopital
from django.utils import timezone
from django.core.exceptions import ValidationError

class Don(models.Model):
    donneur = models.ForeignKey(
        ProfilDonneur,
        on_delete=models.CASCADE,
        related_name='dons'
    )
    
    groupe_sanguin = models.CharField(
        max_length=7,
        choices=ProfilDonneur.GROUPE_SANGUIN,
    )

    hopital = models.ForeignKey(
        Hopital,
        on_delete=models.CASCADE,
        related_name='dons'
    )

    date_don = models.DateField(default=timezone.now)

    volume_ml = models.PositiveIntegerField(default=450, help_text="Volume prélevé en ml")
    
    valide = models.BooleanField(default=False)

    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Don {self.donneur.utilisateur.email} - {self.date_don}"

    def clean(self):
        if not 300 <= self.volume_ml <= 600:
            raise ValidationError(
                {"volume_ml": "Le volume doit être compris entre 300 et 600 ml."}
            )
    
    def save(self, *args, **kwargs):
        if self.pk:
            ancien = Don.objects.get(pk=self.pk)
            if ancien.valide:
                self.groupe_sanguin = ancien.groupe_sanguin
        super().save(*args, **kwargs)

