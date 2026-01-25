def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def common_fields(previous, current):
    return [
        (
            "Cause",
            getattr(previous.cause, "termination_cause", None),
            getattr(current.cause, "termination_cause", None),
        ),
        ("Date", previous.date, current.date),
        ("Authority", previous.authority, current.authority),
        (
            "Status",
            getattr(previous.status, "termination_status", None),
            getattr(current.status, "termination_status", None),
        ),
    ]


def termination_of_appointment_changes(previous, current):
    fields = common_fields(previous, current)
    changes = generate_text(fields)
    return changes


def causes_of_termination_changes(previous, current):
    fields = [
        ("Cause", previous.termination_cause, current.termination_cause),
    ]
    changes = generate_text(fields)
    return changes


def termination_status_changes(previous, current):
    fields = [
        ("Termination Status", previous.termination_status, current.termination_status),
    ]
    changes = generate_text(fields)
    return changes


def incomplete_termination_of_appointment_changes(previous, current):
    fields = common_fields(previous, current)
    fields.append(("Service ID", previous.service_id, current.service_id))
    changes = generate_text(fields)
    return changes
