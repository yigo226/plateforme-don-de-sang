# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path(
        'mes_notifications/',
        views.mes_notifications,
        name='liste'
    ),
    path(
        'detail/<int:notif_id>/',
        views.detail_notification,
        name='detail_notification'
    ),
    path(
        'lire/<int:notification_id>/',
        views.marquer_comme_lu,
        name='lire'
    ),

    path(
        'tout-lire/',
        views.tout_marquer_comme_lu,
        name='tout_lire'
    ),
]
