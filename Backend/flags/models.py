from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from api.models import CustomUser
import logging
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

logger = logging.getLogger(__name__)


class Flags(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=7)
    content_object = GenericForeignKey()  # Abstract column
    flag_type = models.ForeignKey(
        "FlagType", on_delete=models.SET_NULL, null=True, blank=True
    )
    field = models.CharField(max_length=50, null=True, blank=True)
    reason = models.TextField()
    service_id = models.CharField(max_length=7, null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_flags"
    )
    updated_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="updated_flags"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    search_vector = SearchVectorField(null=True)

    class Meta:
        db_table = "flags"
        verbose_name = "flags"
        verbose_name_plural = "flags"

        indexes = [GinIndex(fields=["search_vector"])]

    # Override save method to populate service_id in objects where it is found
    def save(self, *args, **kwargs):
        if not self.service_id and self.content_type and self.object_id:
            model = self.content_type.model_class()

            try:
                obj = model.objects.get(pk=self.object_id)
            except model.DoesNotExist:
                obj = None

            if obj:
                if hasattr(obj, "service_id"):
                    logger.debug(f"{obj} has a 'service_id' attribute")

                    self.service_id = obj.service_id

                elif hasattr(obj, "employee") and obj.employee:
                    logger.debug(
                        f"{obj} has an 'employee' attribute hence must have a 'service_id' attribute"
                    )

                    self.service_id = obj.employee.service_id

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.object_id)} - {self.flag_type}"


class FlagType(models.Model):
    flag_type = models.CharField(max_length=100)

    class Meta:
        db_table = "flag_type"
        verbose_name = "flag_type"

    def __str__(self):
        return self.flag_type
