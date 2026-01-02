from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateAbsencesAPIView.as_view(), name="create-absences"),
    path(
        "<str:pk>/detail/",
        views.RetrieveAbsencesAPIView.as_view(),
        name="retrieve-absences",
    ),
    path(
        "<str:pk>/employee/",
        views.ListEmployeeAbsencesAPIView.as_view(),
        name="list-employee-absences",
    ),
    path("<str:pk>/edit/", views.EditAbsencesAPIView.as_view(), name="edit-absences"),
    path(
        "<str:pk>/delete/",
        views.DeleteAbsencesAPIView.as_view(),
        name="delete-absences",
    ),
]
