from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from demandes.models import DemandeSang
from demandes.models import ReponseDonneur
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification

# Create your views here.
@login_required
def repondre_demande(request, demande_id):
    demande = DemandeSang.objects.get(id=demande_id)
    donneur = request.user.donneur

    ReponseDonneur.objects.create(
        demande=demande,
        donneur=donneur,
        message="Je suis disponible pour ce don."
    )

    # 🔔 notifier le demandeur
    Notification.objects.create(
        destinataire=demande.auteur,
        type=Notification.Type.REPONSE_DONNEUR,
        message=(
            f"Un donneur compatible ({donneur.groupe_sanguin}) "
            f"est disponible pour votre demande."
        ),
        lien=f"/demandes/{demande.id}/"
    )

    return redirect('profil_donneur')

@login_required
def mes_notifications(request):
    notifications = request.user.notifications.order_by('-date_creation')
    return render(
        request,
        'liste.html',
        {'notifications': notifications}
    )


@login_required
def marquer_comme_lu(request, notification_id):
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        destinataire=request.user
    )
    notification.lu = True
    notification.save()
    return redirect(notification.lien or 'notifications:liste')


@login_required
def tout_marquer_comme_lu(request):
    request.user.notifications.filter(lu=False).update(lu=True)
    return redirect('notifications:liste')
