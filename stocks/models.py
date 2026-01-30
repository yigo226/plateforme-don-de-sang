from django.db import models
from hopitaux.models import Hopital
from donneurs.models import ProfilDonneur

# Create your models here.


class StockSang(models.Model):
    hopital = models.ForeignKey(
        Hopital,
        on_delete=models.CASCADE,
        related_name='stocks'
    )

    groupe_sanguin = models.CharField(
        max_length=7,
        choices=ProfilDonneur.GROUPE_SANGUIN
    )

    volume_ml = models.PositiveIntegerField(default=0)

    SEUIL_CRITIQUE = 900  # 2 poches minimum

    class Meta:
        unique_together = ('hopital', 'groupe_sanguin')
        verbose_name = "Stock de sang"
        verbose_name_plural = "Stocks de sang"

    def est_bas(self):
        return self.volume_ml < self.SEUIL_CRITIQUE

    def __str__(self):
        return f"{self.hopital.nom} - {self.groupe_sanguin} ({self.volume_ml} ml)"
