from decimal import Decimal, ROUND_HALF_UP


def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def common_fields(previous, current):
    return [
        # Occurrence
        ("Grade", previous.grade.grade_name, current.grade.grade_name),
        ("Authority", previous.authority, current.authority),
        ("Level|Step", previous.level_step.level_step, current.level_step.level_step),
        ("Monthly Salary", previous.monthly_salary, current.monthly_salary),
        ("Annual Salary", previous.annual_salary, current.annual_salary),
        ("Event", previous.event.event_name, current.event.event_name),
        ("Wef Date", previous.wef_date, current.wef_date),
        ("Reason", previous.reason, current.reason),
    ]


def occurrence_changes(previous, current):
    fields = common_fields(previous, current)
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


def incomplete_occurrence_changes(previous, current):
    fields = common_fields(previous, current)
    fields.append(("Service ID", previous.service_id, current.service_id))
    changes = generate_text(fields)
    return changes
