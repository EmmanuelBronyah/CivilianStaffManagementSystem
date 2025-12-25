from django.urls import path
from . import views

urlpatterns = [
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
]
