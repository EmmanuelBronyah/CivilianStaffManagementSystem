import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .services import generate_employee_excel_report
from celery.result import AsyncResult
from rest_framework import generics
from employees.views import LargeResultsSetPagination
from employees.serializers import EmployeeReadSerializer
from rest_framework.throttling import UserRateThrottle
from .query_builder import build_queryset
from rest_framework.response import Response
from rest_framework import status
from employees.models import Employee
from employees.permissions import IsAdminUserOrStandardUser


logger = logging.getLogger(__name__)


class ListEmployeeRecordsAPIView(generics.GenericAPIView):
    serializer_class = EmployeeReadSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination

    def post(self, request, *args, **kwargs):
        filters = request.data.get("filters")
        qs = build_queryset(Employee, filters)

        serializer = self.get_serializer(qs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EmployeeExportAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrStandardUser]

    def post(self, request):
        filters = request.data.get("filters", [])

        task = generate_employee_excel_report.delay(filters)

        return Response({"message": "Export started successfully", "task_id": task.id})


class ExportStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        result = AsyncResult(task_id)

        if result.status == "SUCCESS":
            return Response({"status": result.status, "file_url": result.result})

        return Response({"status": result.status})
