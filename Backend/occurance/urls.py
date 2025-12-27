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
    # Event
    path("event/", views.ListEventAPIView.as_view(), name="list-event"),
    path(
        "event/create/",
        views.CreateEventAPIView.as_view(),
        name="create-event",
    ),
    path(
        "event/<str:pk>/edit/",
        views.EditEventAPIView.as_view(),
        name="edit-event",
    ),
    path(
        "event/<str:pk>/detail/",
        views.RetrieveEventAPIView.as_view(),
        name="retrieve-event",
    ),
    path(
        "event/<str:pk>/delete/",
        views.DeleteEventAPIView.as_view(),
        name="delete-event",
    ),
    # Salary Adjustment Percentage
    path(
        "percentage-adjustment/",
        views.ListSalaryAdjustmentPercentageAPIView.as_view(),
        name="list-percentage-adjustment",
    ),
    path(
        "percentage-adjustment/create/",
        views.CreateSalaryAdjustmentPercentageAPIView.as_view(),
        name="create-percentage-adjustment",
    ),
    path(
        "percentage-adjustment/<str:pk>/edit/",
        views.EditSalaryAdjustmentPercentageAPIView.as_view(),
        name="edit-percentage-adjustment",
    ),
    path(
        "percentage-adjustment/<str:pk>/detail/",
        views.RetrieveSalaryAdjustmentPercentageAPIView.as_view(),
        name="retrieve-percentage-adjustment",
    ),
    path(
        "percentage-adjustment/<str:pk>/delete/",
        views.DeleteSalaryAdjustmentPercentageAPIView.as_view(),
        name="delete-percentage-adjustment",
    ),
]
