# factory imports
from django.core.management.base import BaseCommand
from abscences.factories import AbsencesFactory
from children.factories import ChildrenFactory, InvalidChildFactory
from courses.factories import CoursesFactory, InvalidCourseFactory
from employees.factories import EmployeeFactory, UnregisteredEmployeesFactory
from identity.factories import IdentityFactory
from marriage.factories import MarriageFactory
from next_of_kin.factories import EmergencyOrNextOfKinFactory
from occurance.factories import OccurrenceFactory, InvalidOccurrenceFactory
from previous_government_service.factories import (
    PreviousGovernmentServiceFactory,
    InvalidPreviousGovernmentServiceFactory,
)
from service_with_forces.factories import (
    ServiceWithForcesFactory,
    InvalidServiceWithForcesFactory,
)
from termination_of_appointment.factories import (
    TerminationOfAppointmentFactory,
    InvalidTerminationOfAppointmentFactory,
)

# model imports
from service_with_forces.models import (
    ServiceWithForces,
    InvalidServiceWithForcesRecords,
)
from termination_of_appointment.models import (
    TerminationOfAppointment,
    InvalidTerminationOfAppointmentRecords,
)
from previous_government_service.models import InvalidPreviousGovernmentServiceRecords
from occurance.models import InvalidOccurrenceRecord
from employees.models import UnregisteredEmployees
from courses.models import InvalidCourseRecords
from children.models import InvalidChildRecords


class Command(BaseCommand):
    help = "Seed the database with many employees efficiently"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, default=1000, help="How many employees to create"
        )

    def handle(self, *args, **options):
        number = options["number"]
        batch_size = 1000
        self.stdout.write(f"Seeding {number} employee records...")

        employees = []

        for i in range(number):
            employees.append(InvalidChildFactory.build())

            if len(employees) >= batch_size:
                InvalidChildRecords.objects.bulk_create(employees)
                employees = []
                self.stdout.write(f"Inserted {i + 1} records...")

        # Insert any remaining records
        if employees:
            InvalidChildRecords.objects.bulk_create(employees)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully seeded {number} employees.")
        )
