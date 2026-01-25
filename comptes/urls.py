
from django.urls import path
from django.contrib.auth import views as auth_views

from comptes.views import accueil

urlpatterns = [
    path('connexion/',
        auth_views.LoginView.as_view(template_name='connexion.html' ),
        name='connexion' ),
    path('', accueil, name='accueil'),

]

