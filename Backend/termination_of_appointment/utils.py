def generate_text(fields):
    changes = [
        f"{label}: {old} → {new}" for label, old, new in fields if str(old) != str(new)
    ]
    return " — ".join(changes)


def termination_of_appointment_changes(previous, current):
    fields = [
        ("Cause", previous.cause, current.cause),
        ("Date", previous.date, current.date),
        ("Authority", previous.authority, current.authority),
        ("Status", previous.status, current.status),
    ]
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
