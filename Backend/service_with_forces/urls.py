from django.urls import path
from . import views

urlpatterns = [
    # Service With Forces
    path(
        "create/",
        views.CreateServiceWithForcesAPIView.as_view(),
        name="create-service-with-forces",
    ),
    path(
        "<str:pk>/detail/",
        views.RetrieveServiceWithForcesAPIView.as_view(),
        name="retrieve-service-with-forces",
    ),
    path(
        "<str:pk>/employee/",
        views.ListEmployeeServiceWithForcesAPIView.as_view(),
        name="list-employee-service-with-forces",
    ),
    path(
        "<str:pk>/edit/",
        views.EditServiceWithForcesAPIView.as_view(),
        name="edit-service-with-forces",
    ),
    path(
        "<str:pk>/delete/",
        views.DeleteServiceWithForcesAPIView.as_view(),
        name="delete-service-with-forces",
    ),
    # Military Ranks
    path(
        "rank/create/",
        views.CreateMilitaryRanksAPIView.as_view(),
        name="create-military-rank",
    ),
    path(
        "rank/<str:pk>/detail/",
        views.RetrieveMilitaryRanksAPIView.as_view(),
        name="retrieve-military-rank",
    ),
    path(
        "rank/",
        views.ListMilitaryRanksAPIView.as_view(),
        name="list-military-rank",
    ),
    path(
        "rank/<str:pk>/edit/",
        views.EditMilitaryRanksAPIView.as_view(),
        name="edit-military-rank",
    ),
    path(
        "rank/<str:pk>/delete/",
        views.DeleteMilitaryRanksAPIView.as_view(),
        name="delete-military-rank",
    ),
]
