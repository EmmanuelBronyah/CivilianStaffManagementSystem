from .utils.retry import network_retry, email_retry
from django.core.cache import cache
import logging
from celery import shared_task
from django_otp.plugins.otp_email.models import EmailDevice


logger = logging.getLogger(__name__)


@network_retry()
def cache_temp_token(temp_token, user_id):
    logger.debug("Set Temporary token in cache.")
    cache.set(temp_token, user_id, timeout=300)


@network_retry()
def get_temp_token(temp_token):
    logger.debug("Retrieving Temporary token from cache.")
    return cache.get(temp_token)


@network_retry()
def delete_temp_token(temp_token):
    cache.delete(temp_token)


@email_retry()
def send_otp_email(device):
    logger.info("Calling generate_challenge()")

    device.generate_challenge()


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def send_otp_email_task(self, device_id):
    try:
        device = EmailDevice.objects.get(id=device_id)

        logger.info(f"Sending OTP email for device {device.id}")
        send_otp_email(device)

    except Exception as e:
        raise self.retry(exc=e)
