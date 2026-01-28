from django.shortcuts import render, redirect
from .models import Utilisateur
from .forms import InscriptionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.

# Accueil
def accueil(request):
    context = {}
    if request.user.is_authenticated:
        context['utilisateur_connecte'] = request.user   
    return render(request, 'index.html', context)

# Inscription d'un DEMANDEUR
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.role = Utilisateur.Role.DEMANDEUR
            utilisateur.set_password(form.cleaned_data['password1'])
            utilisateur.save()
            login(request, utilisateur)
            return redirect('accueil')
    else:
        form = InscriptionForm()

    return render(request, 'inscription.html', {'form': form})


# connexion d'un utilisateur
def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        utilisateur = authenticate(request, email=email, password=password)  # important

        if utilisateur is not None:
            login(request, utilisateur)
            return redirect('accueil')
        else:
            messages.error(request, "Email ou mot de passe incorrect")

    return render(request, 'connexion.html')

# deconnexion d'un utilisateur
def deconnexion(request):
    logout(request)
    return redirect('connexion')


# Profil utilisateur
@login_required
def profil_utilisateur(request):
    user = request.user
    return render(request, 'profil.html',  {'user': user})


# Liste des utilisateurs
@login_required
def liste_utilisateurs(request):

    if request.user.role != request.user.Role.ADMIN:
        raise PermissionDenied
    else:
        utilisateurs = Utilisateur.objects.all()

    return render(request, 'liste_utilisateurs.html', {
        'utilisateurs': utilisateurs
    })
