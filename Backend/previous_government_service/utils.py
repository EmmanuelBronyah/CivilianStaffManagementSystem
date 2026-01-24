def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def common_fields(previous, current):
    return [
        ("Institution", previous.institution, current.institution),
        ("Duration", previous.duration, current.duration),
        ("Position", previous.position, current.position),
    ]


def previous_government_service_changes(previous, current):
    fields = common_fields(previous, current)
    changes = generate_text(fields)
    return changes


def incomplete_previous_government_service_changes(previous, current):
    fields = common_fields(previous, current)
    fields.append(("Service ID", previous.service_id, current.service_id))

    changes = generate_text(fields)
    return changes
