from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Flags


@receiver(post_save, sender=Flags)
def update_flags_search_vector(sender, instance, **kwargs):
    sender.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector("reason", weight="A", config="english")
    )
