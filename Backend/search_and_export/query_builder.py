from employees import models as employee_models
from django.db.models import Q


OPERATOR_MAP = {
    "iexact": "__iexact",
    "gt": "__gt",
    "gte": "__gte",
    "lt": "__lt",
    "lte": "__lte",
    "icontains": "__icontains",
}


def build_queryset(model, filters):
    query = Q()

    for f in filters:
        field = f["field"]
        op = OPERATOR_MAP[f["op"]]
        value = f["value"]

        query &= Q(**{f"{field}{op}": value})

    return model.objects.filter(query)
