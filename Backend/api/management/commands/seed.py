# factory imports
from django.core.management.base import BaseCommand

# from employees.factories import EmployeeFactory, UnregisteredEmployeesFactory

# from abscences.factories import AbsencesFactory

# from children.factories import ChildrenFactory, IncompleteChildFactory

# from courses.factories import CoursesFactory, IncompleteCourseFactory

# from identity.factories import IdentityFactory

# from marriage.factories import MarriageFactory

# from next_of_kin.factories import EmergencyOrNextOfKinFactory

# from occurance.factories import OccurrenceFactory, IncompleteOccurrenceFactory

# from previous_government_service.factories import (
#     PreviousGovernmentServiceFactory,
#     IncompletePreviousGovernmentServiceFactory,
# )

# from service_with_forces.factories import (
#     ServiceWithForcesFactory,
#     IncompleteServiceWithForcesFactory,
# )

from termination_of_appointment.factories import (
    TerminationOfAppointmentFactory,
    IncompleteTerminationOfAppointmentFactory,
)

# model imports
# from service_with_forces.models import (
#     ServiceWithForces,
#     IncompleteServiceWithForcesRecords,
# )

from termination_of_appointment.models import (
    TerminationOfAppointment,
    IncompleteTerminationOfAppointmentRecords,
)

# from occurance.models import IncompleteOccurrence, Occurrence

# from courses.models import IncompleteCourseRecords, Courses

# from children.models import InCompleteChildRecords, Children

# from previous_government_service.models import (
#     IncompletePreviousGovernmentServiceRecords,
#     PreviousGovernmentService,
# )

# from abscences.models import Absences

# from employees.models import Employee
# from employees.models import UnregisteredEmployees
# from marriage.models import Spouse
# from identity.models import Identity
# from next_of_kin.models import EmergencyOrNextOfKin


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
            employees.append(IncompleteTerminationOfAppointmentFactory.build())

            if len(employees) >= batch_size:
                IncompleteTerminationOfAppointmentRecords.objects.bulk_create(employees)
                employees = []
                self.stdout.write(f"Inserted {i + 1} records...")

        # Insert any remaining records
        if employees:
            IncompleteTerminationOfAppointmentRecords.objects.bulk_create(employees)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully seeded {number} employees.")
        )
