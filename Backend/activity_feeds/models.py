from django.db import models
from api.models import CustomUser
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class ActivityFeeds(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    search_vector = SearchVectorField(null=True)

    class Meta:
        db_table = "activity_feeds"
        verbose_name = "activity_feeds"
        verbose_name_plural = "activity_feeds"

        indexes = [GinIndex(fields=["search_vector"])]

    def __str__(self):
        return f"{self.activity} on {self.created_at:%d-%b-%Y %H:%M %p}"
