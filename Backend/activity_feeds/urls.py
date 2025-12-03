from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.ListActivityFeedAPIView.as_view(),
        name="all-activity-feeds",
    )
]
