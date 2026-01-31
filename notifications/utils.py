# utils
from notifications.models import Notification
from donneurs.utils import COMPATIBILITE_SANG
from donneurs.models import ProfilDonneur

def notifier_donneurs(demande):
    donneurs = ProfilDonneur.objects.filter(
        utilisateur__ville__iexact=demande.ville,
        groupe_sanguin__in=COMPATIBILITE_SANG[demande.groupe_sanguin],
    )

    for donneur in donneurs:
        if donneur.peut_donner():
            Notification.objects.create(
                destinataire=donneur.utilisateur,
                type=Notification.Type.DEMANDE_SANG,
                message=(
                    f"Besoin urgent de sang {demande.groupe_sanguin} "
                    f"à {demande.ville}."
                ),
                lien=f"/demandes/{demande.id}/"
            )
