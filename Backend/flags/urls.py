from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListFlagsAPIView.as_view(), name="list-flags"),
    path("create/", views.CreateFlagsAPIView.as_view(), name="create-flag"),
    path("<str:pk>/detail/", views.RetrieveFlagAPIView.as_view(), name="retrieve-flag"),
    path("<str:pk>/edit/", views.EditFlagsAPIView.as_view(), name="edit-flag"),
    path("<str:pk>/delete/", views.DeleteFlagsAPIView.as_view(), name="delete-flag"),
]
