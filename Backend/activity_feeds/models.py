from django.db import models
from api.models import CustomUser


class ActivityFeeds(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "activity_feeds"
        verbose_name = "activity_feeds"
        verbose_name_plural = "activity_feeds"

    def __str__(self):
        return f"{self.activity} on {self.created_at:%d-%b-%Y %H:%M %p}"
