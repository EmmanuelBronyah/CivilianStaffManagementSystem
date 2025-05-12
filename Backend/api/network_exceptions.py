import socket
import ssl
import requests
from urllib.error import URLError
import smtplib
import redis


NETWORK_EXCEPTIONS = (
    socket.gaierror,
    socket.timeout,
    socket.herror,
    socket.error,
    ssl.SSLError,
    ConnectionRefusedError,
    ConnectionAbortedError,
    ConnectionResetError,
    BrokenPipeError,
    TimeoutError,
    # Requests and URL errors
    requests.exceptions.RequestException,
    URLError,
    OSError,
    # smtp errors
    smtplib.SMTPException,
    smtplib.SMTPServerDisconnected,
    smtplib.SMTPConnectError,
    smtplib.SMTPAuthenticationError,
    # Redis errors
    redis.exceptions.ConnectionError,
    redis.exceptions.TimeoutError,
    redis.exceptions.RedisError,
)

# --- DNS & Network Address Errors ---
DNS_ERRORS = (
    socket.gaierror,
    socket.herror,
    URLError,
)

# --- Low-Level Socket & Connection Errors ---
SOCKET_CONNECTION_ERRORS = (
    socket.timeout,
    socket.error,
    ConnectionRefusedError,
    ConnectionAbortedError,
    ConnectionResetError,
    BrokenPipeError,
    TimeoutError,
    OSError,  # Generic OS-level I/O error
)

# --- SSL / Secure Connection Errors ---
SSL_ERRORS = (ssl.SSLError,)

# --- HTTP / Requests Errors ---
HTTP_REQUEST_ERRORS = (requests.exceptions.RequestException,)

# --- Email / SMTP Errors ---
EMAIL_ERRORS = (
    smtplib.SMTPException,
    smtplib.SMTPServerDisconnected,
    smtplib.SMTPConnectError,
    smtplib.SMTPAuthenticationError,
)

# --- Redis Connection Errors ---
REDIS_ERRORS = (
    redis.exceptions.ConnectionError,
    redis.exceptions.TimeoutError,
    redis.exceptions.RedisError,
)
