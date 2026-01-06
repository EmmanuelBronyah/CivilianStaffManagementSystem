from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateNextOfKinAPIView.as_view(), name="create-next-of-kin"),
    path(
        "<str:pk>/detail/",
        views.RetrieveNextOfKinAPIView.as_view(),
        name="retrieve-next-of-kin",
    ),
    path(
        "<str:pk>/employee/",
        views.ListEmployeeNextOfKinAPIView.as_view(),
        name="list-employee-next-of-kin",
    ),
    path(
        "<str:pk>/edit/", views.EditNextOfKinAPIView.as_view(), name="edit-next-of-kin"
    ),
    path(
        "<str:pk>/delete/",
        views.DeleteNextOfKinAPIView.as_view(),
        name="delete-next-of-kin",
    ),
]
