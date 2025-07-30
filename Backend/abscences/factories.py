import factory
import faker
import factory.django
from abscences.models import Absences
from employees.models import Employee
import random


fake = faker.Faker()


class AbsencesFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Absences

    employee = factory.Iterator(Employee.objects.all())
    absence = factory.LazyFunction(lambda: "42 DAYS ANNUAL LEAVE")
    start_date = factory.LazyFunction(fake.date)
    end_date = factory.LazyFunction(fake.date)
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
