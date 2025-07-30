import factory
import faker
import factory.django
from children.models import Children, InvalidChildRecords
from employees import models
import random


fake = faker.Faker()
unique_employees = iter(random.sample(list(models.Employee.objects.all()), 500))


class ChildrenFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Children

    employee = factory.Iterator(models.Employee.objects.all())
    gender = factory.Iterator(models.Gender.objects.all())
    child_name = factory.LazyAttribute(
        lambda obj: (
            fake.name_male() if obj.gender.sex.lower() == "male" else fake.name_female()
        )
    )
    dob = factory.LazyFunction(fake.date)
    other_parent = factory.LazyAttribute(
        lambda obj: (
            fake.name_female()
            if obj.employee.gender.sex.lower() == "male"
            else fake.name_male()
        )
    )
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )


class InvalidChildFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvalidChildRecords

    employee = factory.LazyFunction(lambda: next(unique_employees))
    gender = factory.Iterator(models.Gender.objects.all())
    child_name = factory.LazyAttribute(
        lambda obj: (
            fake.name_male() if obj.gender.sex.lower() == "male" else fake.name_female()
        )
    )
    dob = factory.LazyFunction(lambda: None)
    other_parent = factory.LazyAttribute(
        lambda obj: (
            fake.name_female()
            if obj.employee.gender.sex.lower() == "male"
            else fake.name_male()
        )
    )
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
