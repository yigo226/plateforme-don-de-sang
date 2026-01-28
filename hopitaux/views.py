from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Hopital
from comptes.models import Utilisateur
# Create your views here.

@login_required
def creer_hopital(request):
    if request.user.role != Utilisateur.Role.ADMIN:
        messages.error(request, "Accès refusé.")
        return redirect('accueil')

    if request.method == 'POST':
        nom = request.POST.get('nom')
        ville = request.POST.get('ville')
        telephone = request.POST.get('telephone')

        Hopital.objects.create(
            utilisateur=request.user,
            nom=nom,
            ville=ville,
            telephone=telephone
        )

        request.user.role = Utilisateur.Role.HOPITAL
        request.user.save()

        messages.success(request, "Hôpital créé avec succès.")
        return redirect('dashboard_hopital')

    return render(request, 'creer_hopital.html')

@login_required
def dashboard_hopital(request):
    if request.user.role != Utilisateur.Role.HOPITAL:
        return redirect('accueil')

    hopital = request.user.hopital
    return render(request, 'dashboard.html', {'hopital': hopital})
