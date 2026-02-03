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
    path("api/absences/", include("abscences.urls")),
    path("api/children/", include("children.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/identity/", include("identity.urls")),
    path("api/marriage/", include("marriage.urls")),
    path("api/next-of-kin/", include("next_of_kin.urls")),
    path(
        "api/previous-government-service/", include("previous_government_service.urls")
    ),
    path("api/service-with-forces/", include("service_with_forces.urls")),
    path("api/termination-of-appointment/", include("termination_of_appointment.urls")),
    path("api/search-and-export/", include("search_and_export.urls")),
    path("api/", include("api.urls")),
]


def custom_404_handler(request, exception):
    logger.exception("The requested endpoint does not exist.")
    return JsonResponse(
        {"error": "The requested endpoint does not exist."},
        status=404,
    )


handler404 = "Backend.urls.custom_404_handler"
