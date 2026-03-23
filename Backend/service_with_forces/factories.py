import factory
import faker
import factory.django
from employees.models import Employee, Units
import random
from service_with_forces.models import (
    ServiceWithForces,
    MilitaryRanks,
    IncompleteServiceWithForcesRecords,
)


fake = faker.Faker()
unique_employees = iter(random.sample(list(Employee.objects.all()), 100))


class ServiceWithForcesFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ServiceWithForces

    employee = factory.LazyFunction(lambda: next(unique_employees))
    service_date = factory.LazyFunction(fake.date)
    last_unit = factory.LazyFunction(lambda: random.choice(Units.objects.all()))
    service_id = factory.LazyAttribute(lambda obj: obj.employee.service_id)
    military_rank = factory.LazyFunction(
        lambda: random.choice(MilitaryRanks.objects.all())
    )


class IncompleteServiceWithForcesFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = IncompleteServiceWithForcesRecords

    employee = factory.LazyFunction(lambda: next(unique_employees))
    service_date = factory.LazyFunction(lambda: None)
    last_unit = factory.LazyFunction(lambda: None)
    service_id = factory.LazyAttribute(lambda obj: obj.employee.service_id)
    military_rank = factory.LazyFunction(lambda: None)
