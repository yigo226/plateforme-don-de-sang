from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification

# Create your views here.
@login_required
def mes_notifications(request):
    notifications = request.user.notifications.order_by('-date_creation')
    
    #nb_non_lues = notifications.filter(lu=False).count()
    return render(
        request,
        'liste.html',
        {
            'notifications': notifications,
            #'nb_non_lues': nb_non_lues
        }
    )

@login_required
def detail_notification(request, notif_id):
    notification = get_object_or_404(
        Notification,
        id=notif_id,
        destinataire=request.user
    )

    # Marquer comme lue si elle ne l’est pas encore
    if not notification.lu:
        notification.lu = True
        notification.save()

    return render(
        request,
        'notification_detail.html',
        {
            'notification': notification
        }
    )


@login_required
def marquer_comme_lu(request, notification_id):
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        destinataire=request.user
    )
    notification.lu = True
    notification.save()
    return redirect(notification.lien or 'notifications:liste')

@login_required
def tout_marquer_comme_lu(request):
    request.user.notifications.filter(lu=False).update(lu=True)
    return redirect('notifications:liste')
