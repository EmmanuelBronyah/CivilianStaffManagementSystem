from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
from .. import network_exceptions
import logging

logger = logging.getLogger(__name__)


def network_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type(network_exceptions.NETWORK_EXCEPTIONS),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )


def email_retry():
    return retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception_type(network_exceptions.EMAIL_ERRORS),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
