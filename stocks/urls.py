from django.urls import path
from . import views

urlpatterns = [
    path('hopital/', views.stock_hopital, name='stock_hopital'),
]
