from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_hopital, name='dashboard_hopital'),
    path('creer/', views.creer_hopital, name='creer_hopital'),
]
