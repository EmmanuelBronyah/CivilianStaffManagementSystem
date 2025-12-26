from django.urls import path
from . import views

urlpatterns = [
    # Occurrence
    path("create/", views.CreateOccurrenceAPIView.as_view(), name="create-occurrence"),
    path(
        "<str:pk>/edit/", views.EditOccurrenceAPIView.as_view(), name="edit-occurrence"
    ),
    path(
        "<str:pk>/employee/",
        views.RetrieveEmployeeOccurrenceAPIView.as_view(),
        name="list-employee-occurrence",
    ),
    path(
        "<str:pk>/delete/",
        views.DeleteOccurrenceAPIView.as_view(),
        name="delete-occurrence",
    ),
    # Level|Step
    path("level-step/", views.ListLevelStepAPIView.as_view(), name="list-level-step"),
    path(
        "level-step/create/",
        views.CreateLevelStepAPIView.as_view(),
        name="create-level-step",
    ),
    path(
        "level-step/<str:pk>/edit/",
        views.EditLevelStepAPIView.as_view(),
        name="edit-level-step",
    ),
    path(
        "level-step/<str:pk>/detail/",
        views.RetrieveLevelStepAPIView.as_view(),
        name="retrieve-level-step",
    ),
    path(
        "level-step/<str:pk>/delete/",
        views.DeleteLevelStepAPIView.as_view(),
        name="delete-level-step",
    ),
]
