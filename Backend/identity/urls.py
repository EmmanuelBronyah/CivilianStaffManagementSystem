from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateIdentityAPIView.as_view(), name="create-identity"),
    path(
        "<str:pk>/detail/",
        views.RetrieveEmployeeIdentityAPIView.as_view(),
        name="retrieve-identity",
    ),
    path("<str:pk>/edit/", views.EditIdentityAPIView.as_view(), name="edit-identity"),
    path(
        "<str:pk>/delete/",
        views.DeleteIdentityAPIView.as_view(),
        name="delete-identity",
    ),
]
