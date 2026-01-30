from django.urls import path
from demandes import views

urlpatterns = [
    path('nouvelle/', views.creer_demande, name='creer_demande'),
    path('compatibles/', views.demandes_compatibles, name='demandes_compatibles'),
    path('mes-demandes/', views.mes_demandes, name='mes_demandes'),
    path(
        'cloturer/<int:demande_id>/',
        views.cloturer_demande,
        name='cloturer_demande'
    ),
]
