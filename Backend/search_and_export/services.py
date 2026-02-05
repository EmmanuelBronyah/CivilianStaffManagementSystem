import pandas as pd
from celery import shared_task
from django.conf import settings
from pathlib import Path
from employees.models import Employee
from .query_builder import build_queryset
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)


@shared_task
def generate_employee_excel_report(filters):

    qs = build_queryset(Employee, filters)

    data = qs.values(
        "service_id",
        "last_name",
        "other_names",
        "gender__sex",
        "age",
        "dob",
        "grade__grade_name",
        "unit__unit_name",
        "structure__structure_name",
        "social_security",
        "category",
        "appointment_date",
    )

    df = pd.DataFrame(list(data))

    df.rename(
        columns={
            "service_id": "Service ID",
            "last_name": "Last Name",
            "other_names": "Other Names",
            "gender__sex": "Gender",
            "age": "Age",
            "dob": "Date of Birth",
            "grade__grade_name": "Grade",
            "unit__unit_name": "Unit",
            "structure__structure_name": "Structure",
            "social_security": "Social Security",
            "category": "Category",
            "appointment_date": "Appointment Date",
        },
        inplace=True,
    )

    df.fillna("", inplace=True)

    reports_dir = Path(settings.MEDIA_ROOT) / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    filename = f"employee_report_{uuid4()}.xlsx"
    filepath = reports_dir / filename

    df.to_excel(filepath, index=False, engine="openpyxl")

    logger.info(f"Employee report generated successfully: {filepath}")

    return f"{settings.MEDIA_URL}reports/{filename}"
