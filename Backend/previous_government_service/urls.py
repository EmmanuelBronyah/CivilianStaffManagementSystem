from django.urls import path
from . import views

urlpatterns = [
    path(
        "create/",
        views.CreatePreviousGovernmentServiceAPIView.as_view(),
        name="create-previous-government-service",
    ),
    path(
        "<str:pk>/detail/",
        views.RetrievePreviousGovernmentServiceAPIView.as_view(),
        name="retrieve-previous-government-service",
    ),
    path(
        "<str:pk>/employee/",
        views.ListEmployeePreviousGovernmentServiceAPIView.as_view(),
        name="list-employee-previous-government-service",
    ),
    path(
        "<str:pk>/edit/",
        views.EditPreviousGovernmentServiceAPIView.as_view(),
        name="edit-previous-government-service",
    ),
    path(
        "<str:pk>/delete/",
        views.DeletePreviousGovernmentServiceAPIView.as_view(),
        name="delete-previous-government-service",
    ),
]
