from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from api.models import CustomUser


class FlagType(models.TextChoices):
    DUPLICATE = "DUPLICATE", "Duplicate record"
    INVALID_DATA = "INVALID DATA", "Invalid data"
    POLICY_VIOLATION = "POLICY VIOLATION", "Policy violation"
    NEEDS_REVIEW = "NEEDS REVIEW", "Needs review"


class Flags(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=7)
    content_object = GenericForeignKey()  # Abstract column
    flag_type = models.CharField(max_length=50, choices=FlagType.choices)
    field = models.CharField(max_length=50, null=True, blank=True)
    reason = models.TextField()
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_flags"
    )
    updated_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="updated_flags"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "flags"
        verbose_name = "flags"
        verbose_name_plural = "flags"

    def __str__(self):
        return f"{str(self.content_object)} - {self.flag_type}"
