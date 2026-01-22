def generate_text(fields):
    changes = [
        f"{label}: {old} → {new}" for label, old, new in fields if str(old) != str(new)
    ]
    return " — ".join(changes)


def service_with_forces_changes(previous, current):
    fields = [
        ("Service Date", previous.service_date, current.service_date),
        ("Last Unit", previous.last_unit.unit_name, current.last_unit.unit_name),
        ("Service Number", previous.service_number, current.service_number),
        ("Military Rank", previous.military_rank.rank, current.military_rank.rank),
    ]
    changes = generate_text(fields)
    return changes


def military_rank_changes(previous, current):
    fields = [
        ("Rank", previous.rank, current.rank),
        ("Branch", previous.branch, current.branch),
    ]
    changes = generate_text(fields)
    return changes
