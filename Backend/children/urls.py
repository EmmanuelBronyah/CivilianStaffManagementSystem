from django.urls import path
from . import views

urlpatterns = [
    # children
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
    # incomplete records
    path(
        "incomplete-child-record/create/",
        views.CreateInCompleteChildRecordsAPIView.as_view(),
        name="create-incomplete-child-record",
    ),
    path(
        "incomplete-child-record/<str:pk>/detail/",
        views.RetrieveInCompleteChildRecordsAPIView.as_view(),
        name="retrieve-incomplete-child-record",
    ),
    path(
        "incomplete-child-record/<str:pk>/employee/",
        views.ListEmployeeInCompleteChildRecordsAPIView.as_view(),
        name="list-employee-incomplete-child-record",
    ),
    path(
        "incomplete-child-record/",
        views.ListInCompleteChildRecordsAPIView.as_view(),
        name="list-incomplete-child-record",
    ),
    path(
        "incomplete-child-record/<str:pk>/edit/",
        views.EditInCompleteChildRecordsAPIView.as_view(),
        name="edit-incomplete-child-record",
    ),
    path(
        "incomplete-child-record/<str:pk>/delete/",
        views.DeleteInCompleteChildRecordsAPIView.as_view(),
        name="delete-incomplete-child-record",
    ),
]
