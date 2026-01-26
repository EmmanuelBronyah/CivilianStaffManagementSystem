def generate_text(fields):
    changes = [
        f'{label}: {"N/A" if old == "" or old is None else old} → {"N/A" if new == "" or new is None else new}'
        for label, old, new in fields
        if str(old) != str(new)
    ]
    return " — ".join(changes)


def common_fields(previous, current):
    return [
        ("Service Date", previous.service_date, current.service_date),
        (
            "Last Unit",
            getattr(previous.last_unit, "unit_name", None),
            getattr(current.last_unit, "unit_name", None),
        ),
        ("Service ID", previous.service_id, current.service_id),
        (
            "Military Rank",
            getattr(previous.military_rank, "rank", None),
            getattr(current.military_rank, "rank", None),
        ),
    ]


def service_with_forces_changes(previous, current):
    fields = common_fields(previous, current)
    changes = generate_text(fields)
    return changes


def military_rank_changes(previous, current):
    fields = [
        ("Rank", previous.rank, current.rank),
        ("Branch", previous.branch, current.branch),
    ]
    changes = generate_text(fields)
    return changes


def incomplete_service_with_forces_changes(previous, current):
    fields = common_fields(previous, current)
    changes = generate_text(fields)
    return changes
