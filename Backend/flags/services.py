import logging
from .models import Flags, FlagType
from activity_feeds.models import ActivityFeeds
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)


def create_flag(instance, user):
    flag_type = FlagType.objects.get(flag_type="Incomplete Record")

    flag = Flags.objects.create(
        content_object=instance,
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
            f"{model_name.replace('_', ' ')} was flagged by {user}: "
            f"Flag Type: {flag.flag_type or 'N/A'}"
            f"{flagged_field_text}"
            f" — Reason: {flag.reason}"
        ),
    )
    logger.debug(
        f"Activity feed({model_name.replace('_', ' ')} was flagged by {user}: "
        f"Flag Type: {flag.flag_type or 'N/A'}"
        f"{flagged_field_text}"
        f" — Reason: {flag.reason}"
    )

    return flag


def delete_flag(instance, id, user):
    content_type = ContentType.objects.get_for_model(instance)
    flags = Flags.objects.filter(content_type=content_type, object_id=id)

    model = instance.__class__.__name__.lower()
    model_name = ContentType.objects.get(model=model).name.capitalize()

    for flag in flags:
        logger.debug(f"Flags({flag}) deleted.")

        ActivityFeeds.objects.create(
            creator=user,
            activity=f"{model_name.replace('_', ' ')} flag was deleted by {user}. Flag Type: {flag.flag_type.flag_type.replace('_', ' ').capitalize() or 'None'} — Field: {flag.field.replace('_', ' ').capitalize() or 'None'} — Reason: {flag.reason or 'None'}",
        )

        logger.debug(
            f"Activity feed({model_name.replace('_', ' ')} flag was deleted by {user}. Flag Type: {flag.flag_type.flag_type.replace('_', ' ').capitalize() or 'None'} — Field: {flag.field.replace('_', ' ').capitalize() or 'None'} — Reason: {flag.reason or 'None'}) created."
        )

    Flags.objects.filter(id__in=[flag.id for flag in flags]).delete()

    logger.debug("Flags deletion successful.")
