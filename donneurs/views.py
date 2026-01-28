# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfilDonneurForm, ProfilDonneurUpdateForm
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import get_object_or_404
from comptes.models import Utilisateur

@login_required
def devenir_donneur(request):
    user = request.user
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
    profil = getattr(user, 'role', None)
    if not profil:
        messages.info(request, "Vous n'êtes pas encore donneur.")
        return redirect('devenir_donneur')
    else :
        profil = request.user.profil_donneur
    return render(request, 'profil_donneur.html', {
        'profil': profil,
        'user': user}
        )

# Modifier le profil donneur
@login_required
def modifier_profil_donneur(request):
    profil = request.user.profil_donneur

    if request.method == 'POST':
        form = ProfilDonneurUpdateForm(request.POST, instance=profil)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect('profil_donneur')
    else:
        form = ProfilDonneurUpdateForm(instance=profil)

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

