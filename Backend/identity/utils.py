def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if old != new
    ]
    return " — ".join(changes)


def identity_record_changes(previous, current):
    fields = [
        ("Voters ID", previous.voters_id, current.voters_id),
        ("National ID", previous.national_id, current.national_id),
        ("GLICO ID", previous.glico_id, current.glico_id),
        ("NHIS ID", previous.nhis_id, current.nhis_id),
        ("TIN Number", previous.tin_number, current.tin_number),
    ]
    changes = generate_text(fields)
    return changes
