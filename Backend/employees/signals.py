from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.postgres.search import SearchVector
from .models import Employee
from . import services
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_update(data):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "employees",
        {
            "type": "send_dashboard_stats",
            "event_type": "employee_update",
            "data": data,
        },
    )


def send_employees_dashboard_update():
    total_number_of_employees = services.get_total_number_of_employees()
    employees_per_unit = services.get_two_employee_per_unit_instances()
    total_gender = services.individual_gender_total()
    forecasted_retirees = services.get_forecasted_retirees()
    inactive_employees = services.get_inactive_employees()

    data = {
        "employees_data": {
            "related_data": {
                "total_number_of_employees": total_number_of_employees,
                "inactive_employees": inactive_employees,
            },
            "employees_per_unit": employees_per_unit,
            "total_gender": total_gender,
        },
        "retirement_data": {
            "forecasted_retirees": forecasted_retirees,
        },
    }
    send_update(data)


@receiver(post_save, sender=Employee)
def update_employee_search_vector(sender, instance, created, **kwargs):
    # Update Employee Search Vector field to ensure Employee last name and other names field can be searched
    sender.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector("last_name", weight="A", config="english")
        + SearchVector("other_names", weight="A", config="english")
    )


@receiver(post_save, sender=Employee)
def handle_new_employee_save(sender, instance, created, **kwargs):
    if created:
        send_employees_dashboard_update()


@receiver(post_delete, sender=Employee)
def handle_delete_employee(sender, instance, **kwargs):
    send_employees_dashboard_update()
