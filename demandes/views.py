from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import DemandeSangForm
from demandes.models import DemandeSang, ReponseDonneur
from comptes.models import Utilisateur
from donneurs.utils import COMPATIBILITE_SANG, groupes_receveurs_compatibles
from notifications.utils import notifier_donneurs
from notifications.models import Notification

# Create your views here.


def creer_demande(request):
    if request.method == 'POST':
        form = DemandeSangForm(request.POST, user=request.user)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.auteur = request.user

            if request.user.role == Utilisateur.Role.HOPITAL:
                hopital = request.user.hopital
                demande.hopital = hopital
                demande.ville = hopital.ville

            else:
                demande.volume_ml = 450

            demande.full_clean()
            demande.save()
            notifier_donneurs(demande)
            messages.success(request, "Demande de sang effectuée avec succès.")

            return redirect('mes_demandes')
    else:
        form = DemandeSangForm(user=request.user)

    return render(request, 'creer_demande.html', {'form': form})

@login_required
def demandes_compatibles(request):
    if request.user.role != Utilisateur.Role.DONNEUR:
        messages.error(request, "Accès réservé aux donneurs.")
        return redirect('accueil')

    donneur = request.user.profil_donneur
    from donneurs.utils import groupes_receveurs_compatibles

    groupes_receveurs = groupes_receveurs_compatibles(
        donneur.groupe_sanguin
    )

    demandes = DemandeSang.objects.filter(
        statut=DemandeSang.Statut.ACTIVE,
        ville__iexact=donneur.utilisateur.ville,
        groupe_sanguin__in=groupes_receveurs
    ).order_by('-date_demande')

    return render(
        request,
        'demandes_compatibles.html',
        {'demandes': demandes}
    )

@login_required
def mes_demandes(request):
    demandes = DemandeSang.objects.filter(
        auteur=request.user
    ).order_by('-date_demande')

    return render(
        request,
        'mes_demandes.html',
        {'demandes': demandes}
    )

@login_required
def cloturer_demande(request, demande_id):
    demande = get_object_or_404(
        DemandeSang,
        id=demande_id,
        auteur=request.user
    )

    demande.statut = DemandeSang.Statut.SATISFAITE
    demande.save()

    messages.success(request, "Demande clôturée avec succès.")
    return redirect('mes_demandes')


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

