def generate_text(fields):
    changes = [f"{label}: {old} → {new}" for label, old, new in fields if old != new]
    return " — ".join(changes)


def previous_government_service_changes(previous, current):
    fields = [
        ("Institution", previous.institution, current.institution),
        ("Start Date", previous.start_date, current.start_date),
        ("End Date", previous.end_date, current.end_date),
        ("Position", previous.position, current.position),
    ]
    changes = generate_text(fields)
    return changes
