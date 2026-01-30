from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from stocks.models import StockSang
from comptes.models import Utilisateur
from .models import Don
from .forms import DeclarationDonForm, ValidationDonForm

# ==========================
# DONNEUR
# ==========================

@login_required
def declarer_don(request):
    if request.user.role != Utilisateur.Role.DONNEUR:
        messages.error(request, "Accès réservé aux donneurs.")
        return redirect('accueil')
    else : 
        donneur = request.user.profil_donneur

    if not donneur.peut_donner():
        messages.warning(
            request,
            "Vous ne pouvez pas encore faire un don (délai médical)."
        )
        return redirect('profil_donneur')

    if request.method == 'POST':
        form = DeclarationDonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.donneur = donneur
            don.groupe_sanguin = donneur.groupe_sanguin
            don.save()

            messages.success(
                request,
                "Don déclaré. En attente de validation par l’hôpital."
            )
            return redirect('profil_donneur')
    else:
        form = DeclarationDonForm()

    return render(request, 'declarer_don.html', {'form': form})


# ==========================
# HÔPITAL
# ==========================

@login_required
def dons_a_valider(request):
    if request.user.role != Utilisateur.Role.HOPITAL:
        messages.error(request, "Accès refusé.")
        return redirect('accueil')
    else:
        hopital = request.user.hopital  
    dons = Don.objects.filter(
        hopital=hopital,
        valide=False
    ).order_by('-date_don')

    return render(request, 'dons_a_valider.html', {'dons': dons})

@login_required
def valider_don(request, don_id):
    if request.user.role != Utilisateur.Role.HOPITAL:
        messages.error(request, "Accès refusé.")
        return redirect('accueil')

    hopital = request.user.hopital
    don = get_object_or_404(Don, id=don_id, hopital=hopital, valide=False)

    if request.method == 'POST':
        form = ValidationDonForm(request.POST, instance=don)
        if form.is_valid():
            don = form.save(commit=False)
            don.valide = True
            don.save()

            donneur = don.donneur
            donneur.date_dernier_don = don.date_don
            don.groupe_sanguin = donneur.groupe_sanguin
            donneur.save()

            stock, created = StockSang.objects.get_or_create(
                hopital=hopital,
                groupe_sanguin=don.groupe_sanguin
            )

            stock.volume_ml += don.volume_ml
            stock.save()

            messages.success(request, "Don validé avec succès.")
            return redirect('dons_a_valider')
    else:
        form = ValidationDonForm(instance=don)

    return render(
        request,
        'valider_don.html',
        {'form': form, 'don': don}
    )

# @login_required
# def valider_don(request, don_id):
#     if request.user.role != Utilisateur.Role.HOPITAL:
#         messages.error(request, "Accès refusé.")
#         return redirect('accueil')
#     else : 
#         hopital = request.user.hopital

#     don = get_object_or_404(Don, id=don_id, hopital=hopital)

#     don.valide = True
#     don.save()

#     donneur = don.donneur
#     donneur.date_dernier_don = don.date_don
#     donneur.save()

#     messages.success(request, "Don validé avec succès.")
#     return redirect('dons_a_valider')
