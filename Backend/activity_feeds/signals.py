from .models import ActivityFeeds
from django.contrib.postgres.search import SearchVector, Value
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=ActivityFeeds)
def update_activity_feeds_search_vector(sender, instance, **kwargs):
    if hasattr(instance, "_search_vector_updated"):
        return

    instance._search_vector_updated = True

    instance.search_vector = SearchVector(
        Value(instance.activity), weight="A", config="english"
    ) + SearchVector(Value(instance.creator.username), weight="B", config="english")

    instance.save(update_fields=["search_vector"])
