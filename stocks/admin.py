from django.contrib import admin
from .models import StockSang
# Register your models here.

@admin.register(StockSang)
class StockSangAdmin(admin.ModelAdmin):
    list_display = ('hopital', 'groupe_sanguin', 'volume_ml')
    list_filter = ('hopital', 'groupe_sanguin')
