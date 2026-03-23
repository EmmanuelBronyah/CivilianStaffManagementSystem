import factory
import faker
import factory.django
from employees import models
import random
from previous_government_service.models import (
    PreviousGovernmentService,
    IncompletePreviousGovernmentServiceRecords,
)

fake = faker.Faker()
unique_employees = iter(random.sample(list(models.Employee.objects.all()), 100))


class PreviousGovernmentServiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = PreviousGovernmentService

    employee = factory.LazyFunction(lambda: next(unique_employees))
    institution = factory.LazyFunction(fake.city)
    duration = factory.LazyFunction(lambda: f"{fake.date()} to {fake.date()}")
    position = factory.LazyFunction(fake.job)


class IncompletePreviousGovernmentServiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = IncompletePreviousGovernmentServiceRecords

    employee = factory.LazyFunction(lambda: next(unique_employees))
    institution = factory.LazyFunction(lambda: None)
    duration = factory.LazyFunction(lambda: None)
    position = factory.LazyFunction(fake.job)
