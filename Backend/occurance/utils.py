from .models import Event, LevelStep
from decimal import Decimal, ROUND_HALF_UP


def generate_text(fields):
    changes = [f"{label}: {old} → {new}" for label, old, new in fields if old != new]
    return " — ".join(changes)


def occurrence_changes(previous, current):
    fields = [
        # Occurrence
        ("Grade", previous.grade.grade_name, current.grade.grade_name),
        ("Authority", previous.authority, current.authority),
        ("Level|Step", previous.level_step.level_step, current.level_step.level_step),
        ("Monthly Salary", previous.monthly_salary, current.monthly_salary),
        ("Annual Salary", previous.annual_salary, current.annual_salary),
        ("Event", previous.event.event, current.event.event),
        ("Wef Date", previous.wef_date, current.wef_date),
        ("Reason", previous.reason, current.reason),
    ]
    changes = generate_text(fields)
    return changes


def level_step_changes(previous, current):
    fields = [
        ("Level|Step", previous.level_step, current.level_step),
        ("Monthly Salary", previous.monthly_salary, current.monthly_salary),
    ]
    changes = generate_text(fields)
    return changes


def two_dp(figure):
    return Decimal(str(figure)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def update_occurrence_salaries(occurrence_data):
    data = occurrence_data if isinstance(occurrence_data, list) else [occurrence_data]

    for occurrence in data:
        event_id = occurrence["event"]
        event = Event.objects.get(id=event_id).event_name

        level_step_id = occurrence["level_step"]
        monthly_salary = LevelStep.objects.get(id=level_step_id).monthly_salary
        monthly_salary = two_dp(monthly_salary)

        if event != "Salary Adjustment":

            occurrence["monthly_salary"] = str(monthly_salary)

            annual_salary = two_dp(two_dp(12) * monthly_salary)
            occurrence["annual_salary"] = str(annual_salary)

        else:
            percentage_adjustment = occurrence.pop("percentage_adjustment")
            percentage_adjustment = two_dp(int(percentage_adjustment) / 100)

            monthly_salary = two_dp(
                (two_dp(monthly_salary * percentage_adjustment)) + monthly_salary
            )
            occurrence["monthly_salary"] = str(monthly_salary)

            annual_salary = two_dp(two_dp(12) * monthly_salary)
            occurrence["annual_salary"] = str(annual_salary)

    return occurrence_data
