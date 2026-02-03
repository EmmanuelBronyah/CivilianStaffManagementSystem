from django.apps import AppConfig


class ActivityFeedsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "activity_feeds"

    def ready(self):
        import activity_feeds.signals
