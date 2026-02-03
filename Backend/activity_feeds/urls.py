from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.ListActivityFeedAPIView.as_view(),
        name="all-activity-feeds",
    ),
    path(
        "search/",
        views.SearchActivityAPIView.as_view(),
        name="search-activity-feeds",
    ),
]
