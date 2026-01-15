import logging
from .models import Flags, FlagType
from django.contrib.contenttypes.models import ContentType
from activity_feeds.models import ActivityFeeds

logger = logging.getLogger(__name__)


def create_flag(instance, user):
    model_name = instance.__class__.__name__.lower()
    content_type = ContentType.objects.get(model=model_name)

    flag_type = FlagType.objects.get(flag_type="Incomplete Record")

    flag = Flags.objects.create(
        content_type=content_type,
        object_id=instance.id,
        flag_type=flag_type,
        field="All",
        reason="Incomplete Record",
        service_id=instance.service_id,
        created_by=user,
        updated_by=user,
    )

    logger.debug(f"Flags({flag}) created.")

    model_name = flag.content_type.name.capitalize()

    flagged_field_text = (
        f" — Flagged Field: {flag.field.replace('_', ' ').capitalize()}"
        if flag.field
        else "N/A"
    )

    ActivityFeeds.objects.create(
        creator=user,
        activity=(
            f"{model_name} Record was flagged by {user}: "
            f"Flag Type: {flag.flag_type or 'N/A'}"
            f"{flagged_field_text}"
            f" — Reason: {flag.reason}"
        ),
    )
    logger.debug(
        f"Activity feed({model_name} Record was flagged by {user}: "
        f"Flag Type: {flag.flag_type or 'N/A'}"
        f"{flagged_field_text}"
        f" — Reason: {flag.reason}"
    )

    return flag
