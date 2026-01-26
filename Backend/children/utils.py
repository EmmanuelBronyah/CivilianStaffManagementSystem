def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def common_fields(previous, current):
    return [
        ("Child Name", previous.child_name, current.child_name),
        ("Date of Birth", previous.dob, current.dob),
        (
            "Gender",
            getattr(previous.gender, "sex", None),
            getattr(current.gender, "sex", None),
        ),
        ("Other Parent", previous.other_parent, current.other_parent),
        ("Authority", previous.authority, current.authority),
    ]


def child_record_changes(previous, current):
    fields = common_fields(previous, current)
    changes = generate_text(fields)
    return changes


def incomplete_child_record_changes(previous, current):
    fields = common_fields(previous, current)
    fields.append(("Service ID", previous.service_id, current.service_id))

    changes = generate_text(fields)
    return changes
