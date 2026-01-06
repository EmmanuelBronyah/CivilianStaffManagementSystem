from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateSpouseAPIView.as_view(), name="create-spouse"),
    path(
        "<str:pk>/detail/",
        views.RetrieveSpouseAPIView.as_view(),
        name="retrieve-spouse",
    ),
    path(
        "<str:pk>/employee/",
        views.ListEmployeeSpouseAPIView.as_view(),
        name="list-employee-spouse",
    ),
    path("<str:pk>/edit/", views.EditSpouseAPIView.as_view(), name="edit-spouse"),
    path(
        "<str:pk>/delete/",
        views.DeleteSpouseAPIView.as_view(),
        name="delete-spouse",
    ),
]
