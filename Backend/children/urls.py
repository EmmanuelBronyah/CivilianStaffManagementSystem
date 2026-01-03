from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateChildRecordAPIView.as_view(), name="create-child"),
    path(
        "<str:pk>/detail/",
        views.RetrieveChildRecordAPIView.as_view(),
        name="retrieve-child",
    ),
    path(
        "<str:pk>/employee/",
        views.ListEmployeeChildrenAPIView.as_view(),
        name="list-employee-children",
    ),
    path("<str:pk>/edit/", views.EditChildRecordAPIView.as_view(), name="edit-child"),
    path(
        "<str:pk>/delete/",
        views.DeleteChildRecordAPIView.as_view(),
        name="delete-child",
    ),
]
