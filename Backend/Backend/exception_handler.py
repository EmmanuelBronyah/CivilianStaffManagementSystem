from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from api import network_exceptions
import logging
from rest_framework.exceptions import ValidationError
from .utils import handle_validation_error
from django.db.models.deletion import ProtectedError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # DNS/Host resolution errors
    if isinstance(exc, network_exceptions.DNS_ERRORS):
        logger.exception(
            "A DNS Error occurred. We couldn't reach the server. Please check your internet connection or try again later."
        )
        return Response(
            {
                "error": "We couldn't reach the server. Please check your internet connection or try again later."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Socket/Connection issues
    elif isinstance(exc, network_exceptions.SOCKET_CONNECTION_ERRORS):
        logger.exception(
            "A Socket Connection Error occurred. Network issue detected. Please ensure you are connected to the internet and try again."
        )
        return Response(
            {
                "error": "Network issue detected. Please ensure you are connected to the internet and try again."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # SSL certificate or secure connection problems
    elif isinstance(exc, network_exceptions.SSL_ERRORS):
        logger.exception(
            "An SSL Error occurred. Secure connection failed. Please check your network or contact support."
        )
        return Response(
            {
                "error": "Secure connection failed. Please check your network or contact support."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Requests/HTTP errors
    elif isinstance(exc, network_exceptions.HTTP_REQUEST_ERRORS):
        logger.exception(
            "An HTTP Request Error has occurred. We couldn't complete the request. Please try again or check your internet connection."
        )
        return Response(
            {
                "error": "We couldn't complete the request. Please try again or check your internet connection."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # SMTP / Email related issues
    elif isinstance(exc, network_exceptions.EMAIL_ERRORS):
        logger.exception(
            "An Email Error has occurred. We couldn't send an email right now. Please try again later."
        )
        return Response(
            {"error": "We couldn't send an email right now. Please try again later."},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    # Redis connection errors
    elif isinstance(exc, network_exceptions.REDIS_ERRORS):
        logger.exception(
            "A Redis Error has occurred. Temporary server issue. Please try again shortly."
        )
        return Response(
            {"error": "Temporary server issue. Please try again shortly."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Handles all validation errors
    # elif isinstance(exc, ValidationError):
    #     message = handle_validation_error(exc)
    #     logger.exception(message)
    #     return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

    elif isinstance(exc, ProtectedError):
        return Response(
            {"error": "This record cannot be deleted because it is currently in use."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    else:
        # Fall back to default handler
        logger.exception(f"An Exception({exc}) has occurred.")
        return exception_handler(exc, context)
