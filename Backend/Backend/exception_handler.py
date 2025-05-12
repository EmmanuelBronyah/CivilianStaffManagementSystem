from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from api import network_exceptions


def custom_exception_handler(exc, context):
    # DNS/Host resolution errors
    if isinstance(exc, network_exceptions.DNS_ERRORS):
        return Response(
            {
                "error": "We couldn't reach the server. Please check your internet connection or try again later."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Socket/Connection issues
    elif isinstance(exc, network_exceptions.SOCKET_CONNECTION_ERRORS):
        return Response(
            {
                "error": "Network issue detected. Please ensure you are connected to the internet and try again."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # SSL certificate or secure connection problems
    elif isinstance(exc, network_exceptions.SSL_ERRORS):
        return Response(
            {
                "error": "Secure connection failed. Please check your network or contact support."
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    # Requests/HTTP errors
    elif isinstance(exc, network_exceptions.HTTP_REQUEST_ERRORS):
        return Response(
            {
                "error": "We couldn't complete the request. Please try again or check your internet connection."
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # SMTP / Email related issues
    elif isinstance(exc, network_exceptions.EMAIL_ERRORS):
        return Response(
            {"error": "We couldn't send an email right now. Please try again later."},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    # Redis connection errors
    elif isinstance(exc, network_exceptions.REDIS_ERRORS):
        return Response(
            {"error": "Temporary server issue. Please try again shortly."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    else:
        # Fall back to default handler
        return exception_handler(exc, context)
