import factory
import faker
import factory.django
from employees.models import Employee
import random
from termination_of_appointment.models import (
    TerminationOfAppointment,
    CausesOfTermination,
    TerminationStatus,
    InvalidTerminationOfAppointmentRecords,
)


fake = faker.Faker()
unique_employees = iter(random.sample(list(Employee.objects.all()), 400))


class TerminationOfAppointmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TerminationOfAppointment

    employee = factory.LazyFunction(lambda: next(unique_employees))
    cause = factory.LazyFunction(lambda: CausesOfTermination.objects.get(id=2))
    date = factory.LazyFunction(fake.date)
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
    status = factory.LazyFunction(lambda: TerminationStatus.objects.get(id=2))


class InvalidTerminationOfAppointmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvalidTerminationOfAppointmentRecords

    employee = factory.LazyFunction(lambda: next(unique_employees))
    cause = factory.LazyFunction(lambda: None)
    date = factory.LazyFunction(lambda: None)
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
    status = factory.LazyFunction(lambda: None)
