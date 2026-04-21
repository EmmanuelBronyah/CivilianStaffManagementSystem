from django.db.models import Count, Q
from employees import models
from datetime import datetime
from django.db.models.functions import ExtractYear
from django.db.models import F
from activity_feeds.models import ActivityFeeds
from termination_of_appointment.models import TerminationOfAppointment
from api.models import CustomUser, Divisions


def get_users_per_role():
    return CustomUser.objects.aggregate(
        administrators=Count("role", filter=Q(role="ADMINISTRATOR")),
        standard_users=Count("role", filter=Q(role="STANDARD USER")),
        viewers=Count("role", filter=Q(role="VIEWER")),
    )


def get_total_number_of_employees():
    return models.Employee.objects.count()


def get_two_employee_per_unit_instances():
    units = models.Units.objects.annotate(total_employees=Count("employee")).order_by(
        "-total_employees"
    )[:2]
    return [{unit.unit_name: unit.total_employees} for unit in units]


def individual_gender_total():
    genders = models.Gender.objects.annotate(total_employees=Count("employee"))
    return [{"name": gender.sex, "value": gender.total_employees} for gender in genders]


def get_current_year_and_end_year(number_of_years):
    current_year = datetime.now().year
    end_year = current_year + number_of_years - 1
    return current_year, end_year


def get_retirement_label():
    number_of_years = 11
    current_year, end_year = get_current_year_and_end_year(number_of_years)
    return f"Projected Retirements ({current_year}-{end_year})"


def get_forecasted_retirees():
    number_of_years = 11
    current_year, end_year = get_current_year_and_end_year(number_of_years)

    # Annotate retirement year
    employees = (
        models.Employee.objects.annotate(retirement_year=ExtractYear(F("dob")) + 60)
        .filter(retirement_year__range=(current_year, end_year))
        .values("service_id", "retirement_year")
    )

    # Group employees by year
    grouped = {}

    for emp in employees:
        year = emp["retirement_year"]
        grouped.setdefault(year, []).append(emp["service_id"])

    # Build results
    forecasted_retirees_results = []

    for offset in range(number_of_years):
        year = current_year + offset
        employee_ids = grouped.get(year, [])

        forecasted_retirees_results.append(
            {"year": year, "count": len(employee_ids), "employees": employee_ids}
        )

    return forecasted_retirees_results


def get_inactive_employees():
    return TerminationOfAppointment.objects.count()


def get_sample_activity_feeds():
    feeds = ActivityFeeds.objects.select_related("creator").order_by("-created_at")[:10]
    return [
        {
            "id": feed.id,
            "creator": feed.creator.username,
            "activity": feed.activity,
            "created_at": feed.created_at.strftime("%d-%b-%Y %I:%M %p"),
        }
        for feed in feeds
    ]


def get_divisions():
    return Divisions.objects.all()


def get_grades():
    return models.Grades.objects.all()


def get_marital_status():
    return models.MaritalStatus.objects.all()


def get_gender():
    return models.Gender.objects.all()


def get_structure():
    return models.Structure.objects.all()


def get_units():
    return models.Units.objects.all()


def get_region():
    return models.Region.objects.all()


def get_religion():
    return models.Religion.objects.all()


def get_blood_group():
    return models.BloodGroup.objects.all()
