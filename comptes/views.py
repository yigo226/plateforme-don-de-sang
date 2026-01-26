from django.shortcuts import render, redirect
from .models import Utilisateur
from .forms import InscriptionDonneurForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

# Page d'accueil
def accueil(request):
    return render(request, 'index.html')

# Inscription d'un donneur
def inscription(request):
    if request.method == 'POST':
        form = InscriptionDonneurForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.role = Utilisateur.Role.DONNEUR
            utilisateur.set_password(form.cleaned_data['password1'])
            utilisateur.save()
            login(request, utilisateur)
            return redirect('accueil')
    else:
        form = InscriptionDonneurForm()

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


# Liste des utilisateurs
def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'liste_utilisateurs.html', {
        'utilisateurs': utilisateurs
    })
