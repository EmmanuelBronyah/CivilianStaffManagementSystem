def occurrence_changes(previous, current):
    fields = [
        ("Grade", previous.grade.grade_name, current.grade.grade_name),
        ("Authority", previous.authority, current.authority),
        ("Level|Step", previous.level_step.level_step, current.level_step.level_step),
        ("Monthly Salary", previous.monthly_salary, current.monthly_salary),
        ("Annual Salary", previous.annual_salary, current.annual_salary),
        ("Event", previous.event.event, current.event.event),
        ("Wef Date", previous.wef_date, current.wef_date),
        ("Reason", previous.reason, current.reason),
    ]

    changes = [f"{label}: {old} → {new}" for label, old, new in fields if old != new]

    return " — ".join(changes)
