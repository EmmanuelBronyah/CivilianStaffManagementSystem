from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListFlagsAPIView.as_view(), name="list-flags"),
    path("search/", views.SearchFlagsAPIView.as_view(), name="search-flags"),
    path("create/", views.CreateFlagsAPIView.as_view(), name="create-flag"),
    path("<str:pk>/detail/", views.RetrieveFlagAPIView.as_view(), name="retrieve-flag"),
    path("<str:pk>/edit/", views.EditFlagsAPIView.as_view(), name="edit-flag"),
    path("<str:pk>/delete/", views.DeleteFlagsAPIView.as_view(), name="delete-flag"),
    # flag type
    path("type/", views.ListFlagTypeAPIView.as_view(), name="list-flag-type"),
    path(
        "type/create/", views.CreateFlagTypeAPIView.as_view(), name="create-flag-type"
    ),
    path(
        "type/<str:pk>/detail/",
        views.RetrieveFlagTypeAPIView.as_view(),
        name="retrieve-flag-type",
    ),
    path(
        "type/<str:pk>/edit/",
        views.EditFlagTypeAPIView.as_view(),
        name="edit-flag-type",
    ),
    path(
        "type/<str:pk>/delete/",
        views.DeleteFlagTypeAPIView.as_view(),
        name="delete-flag-type",
    ),
]
