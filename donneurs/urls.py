from django.urls import path
from . import views

urlpatterns = [
    path('devenir/', views.devenir_donneur, name='devenir_donneur'),
    path('profil/', views.profil_donneur, name='profil_donneur'),
    path('modifier/', views.modifier_profil_donneur, name='modifier_profil_donneur'),
]
