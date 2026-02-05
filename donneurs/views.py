# Create your views here.
from dataclasses import field
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfilDonneurForm, ProfilDonneurUpdateForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from comptes.models import Utilisateur
from django.core.exceptions import PermissionDenied
from notifications.models import Notification

@login_required
def devenir_donneur(request):
    user = request.user

    # ADMIN et HÔPITAL interdits
    if user.role in [user.Role.ADMIN, user.Role.HOPITAL]:
        raise PermissionDenied("Accès réservé aux donneurs")

    if hasattr(user, 'donneur'):
        messages.info(request, "Vous êtes déjà donneur.")
        return redirect('profil_utilisateur')

    if request.method == 'POST':
        form = ProfilDonneurForm(request.POST)
        if form.is_valid():
            profil = form.save(commit=False)
            profil.utilisateur = user
            profil.save()
            user.role = user.Role.DONNEUR
            user.save()
            messages.success(request, "Vous êtes maintenant un donneur !")
            return redirect('profil_utilisateur')
    else:
        form = ProfilDonneurForm()

    return render(request, 'devenir_donneur.html', {'form': form})

# Profil donneur
@login_required
def profil_donneur(request):
    user = request.user

    # ADMIN et HÔPITAL interdits
    if user.role in [user.Role.ADMIN, user.Role.HOPITAL]:
        raise PermissionDenied("Accès réservé aux donneurs")

    # Utilisateur normal mais pas encore donneur
    if user.role != user.Role.DONNEUR:
        messages.info(request, "Vous n'êtes pas encore donneur.")
        return redirect('devenir_donneur')

    # DONNEUR : on récupère son profil
    profil = user.profil_donneur

    return render(request, 'profil_donneur.html', {
        'profil': profil,
        'user': user
    })


# Modifier le profil donneur
@login_required
def modifier_profil_donneur(request):
    # ADMIN et HÔPITAL interdits
    if request.user.role in [request.user.Role.ADMIN, request.user.Role.HOPITAL, request.user.Role.DEMANDEUR]:
        raise PermissionDenied("Accès réservé aux donneurs")
    else :
        profil = request.user.profil_donneur

        if request.method == 'POST':
            form = ProfilDonneurUpdateForm(request.POST, instance=profil)
            

            if form.is_valid():
                form.save()
                messages.success(request, "Profil mis à jour.")
                return redirect('profil_donneur')
        else:
            form = ProfilDonneurUpdateForm(instance=profil)
    
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
    return render(request, 'modifier_profil.html', {'form': form})

# @login_required
# def modifier_profil_donneur(request):
#     user = request.user
#     profil = get_object_or_404(ProfilDonneur, utilisateur=user)

#     if request.method == 'POST':
#         form = ProfilDonneurUpdateForm(request.POST, instance=profil)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Votre profil donneur a été mis à jour.")
#             return redirect('profil_donneur')
#     else:
#         form = ProfilDonneurUpdateForm(instance=profil)

#     return render(request, 'modifier_profil.html', {'form': form})

@login_required
def dashboard_don(request):

    if request.user.role != Utilisateur.Role.DONNEUR:
            messages.error(request, "Accès réservé aux donneurs.")
            return redirect('accueil')  
    # nombre de notifications non lues pour le donneur
    
    else: 
        profil = request.user.profil_donneur
        nb_non_lues = request.user.notifications.filter(lu=False).count()
        
        return render(request, 'dashboard_donneur.html', {'profil': profil, 'nb_non_lues': nb_non_lues})
