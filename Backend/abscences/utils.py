def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def absences_changes(previous, current):
    fields = [
        # Occurrence
        ("Absence", previous.absence, current.absence),
        ("Authority", previous.authority, current.authority),
        ("Start Date", previous.start_date, current.start_date),
        ("End Date", previous.end_date, current.end_date),
    ]
    changes = generate_text(fields)
    return changes
