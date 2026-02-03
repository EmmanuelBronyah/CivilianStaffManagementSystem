from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import ActivityFeeds


@receiver(post_save, sender=ActivityFeeds)
def update_activity_feeds_search_vector(sender, instance, **kwargs):
    sender.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector("activity", weight="A", config="english")
        + SearchVector("creator__username", weight="B", config="english")
    )
