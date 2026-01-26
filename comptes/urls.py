
from django.urls import path
from comptes import views 

urlpatterns = [
    # Accueil
    path('', views.accueil, name='accueil'),

    # inscription d'un donneur
    path('inscription/', views.inscription, name='inscription'),

    # Connexion et deconnexion
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    #liste des utilisateurs
    path('users/', views.liste_utilisateurs, name='liste_utilisateurs'),
    
]
