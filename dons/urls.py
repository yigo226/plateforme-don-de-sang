from django.urls import path
from . import views

urlpatterns = [
    # Donneur
    path('declarer/', views.declarer_don, name='declarer_don'),

    # Hôpital
    path('a-valider/', views.dons_a_valider, name='dons_a_valider'),
    path('valider/<int:don_id>/', views.valider_don, name='valider_don'),
]
