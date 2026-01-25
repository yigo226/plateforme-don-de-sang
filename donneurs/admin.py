from django.contrib import admin

# Register your models here.
from .models import ProfilDonneur

@admin.register(ProfilDonneur)
class ProfilDonneurAdmin(admin.ModelAdmin):
    list_display = (
        'utilisateur',
        'poids',
        'groupe_sanguin',
        'groupe_sanguin_verrouille',
    )
