from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
import logging


logger = logging.getLogger(__name__)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/employees/", include("employees.urls")),
    path("api/activity-feeds/", include("activity_feeds.urls")),
    path("api/flags/", include("flags.urls")),
    path("api/occurrence/", include("occurance.urls")),
    path("api/", include("api.urls")),
]


def custom_404_handler(request, exception):
    logger.exception("The requested endpoint does not exist.")
    return JsonResponse(
        {"error": "The requested endpoint does not exist."},
        status=404,
    )


handler404 = "Backend.urls.custom_404_handler"
