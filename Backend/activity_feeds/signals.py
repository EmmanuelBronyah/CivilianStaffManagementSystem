from .models import ActivityFeeds
from django.contrib.postgres.search import SearchVector, Value
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from employees import services


def send_update(data):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "feeds",
        {"type": "send_dashboard_stats", "event_type": "feeds_update", "data": data},
    )


def send_feeds_dashboard_update():
    data = services.get_sample_activity_feeds()
    send_update(data)


@receiver(post_save, sender=ActivityFeeds)
def update_activity_feeds_search_vector(sender, instance, **kwargs):
    if hasattr(instance, "_search_vector_updated"):
        return

    instance._search_vector_updated = True

    instance.search_vector = SearchVector(
        Value(instance.activity), weight="A", config="english"
    ) + SearchVector(Value(instance.creator.username), weight="B", config="english")

    instance.save(update_fields=["search_vector"])


@receiver(post_save, sender=ActivityFeeds)
def handle_add_new_activity_feed(sender, instance, created, **kwargs):
    if created:
        send_feeds_dashboard_update()
