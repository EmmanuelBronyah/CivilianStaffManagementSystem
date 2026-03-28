from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from .models import CustomUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from employees import services


def send_update(data):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "users",
        {
            "type": "send_dashboard_stats",
            "event_type": "user_update",
            "data": data,
        },
    )


def send_users_dashboard_update():
    data = services.get_users_per_role()
    send_update(data)


@receiver(post_save, sender=CustomUser)
def handle_new_user_save(sender, instance, created, **kwargs):
    if created:
        send_users_dashboard_update()


@receiver(post_delete, sender=CustomUser)
def handle_user_delete(sender, instance, **kwargs):
    send_users_dashboard_update()
