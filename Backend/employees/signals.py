from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.postgres.search import SearchVector
from .models import Employee


@receiver(post_save, sender=Employee)
def update_employee_search_vector(sender, instance, **kwargs):
    sender.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector("last_name", weight="A", config="english")
        + SearchVector("other_names", weight="A", config="english")
    )
