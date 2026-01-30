
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from comptes.models import Utilisateur
from .models import StockSang

# Create your views here.

@login_required
def stock_hopital(request):
    if request.user.role != Utilisateur.Role.HOPITAL:
        messages.error(request, "Accès refusé.")
        return redirect('accueil')

    hopital = request.user.hopital

    stocks = StockSang.objects.filter(hopital=hopital)

    return render(
        request,
        'stock_hopital.html',
        {'stocks': stocks}
    )
