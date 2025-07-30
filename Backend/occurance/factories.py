import factory
import faker
import factory.django
from employees.models import Employee
import random
from occurance.models import Occurrence, LevelStep, Event, InvalidOccurrenceRecord


fake = faker.Faker()
unique_employees = iter(random.sample(list(Employee.objects.all()), 6000))


class OccurrenceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Occurrence

    employee = factory.Iterator(Employee.objects.all())
    grade = factory.LazyAttribute(lambda obj: obj.employee.grade)
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
    level_step = factory.LazyFunction(lambda: random.choice(LevelStep.objects.all()))
    monthly_salary = factory.LazyAttribute(lambda obj: obj.level_step.monthly_salary)
    annual_salary = factory.LazyAttribute(
        lambda obj: 12 * obj.level_step.monthly_salary
    )
    event = factory.LazyFunction(lambda: Event.objects.get(id=14))
    wef_date = factory.LazyFunction(fake.date)
    reason = factory.LazyFunction(lambda: "Newly Employed")


class InvalidOccurrenceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvalidOccurrenceRecord

    employee = factory.LazyFunction(lambda: next(unique_employees))
    grade = factory.LazyAttribute(lambda obj: obj.employee.grade)
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
    level_step = factory.LazyAttribute(
        lambda obj: obj.employee.occurrence_set.all()[0].level_step
    )
    monthly_salary = factory.LazyAttribute(lambda obj: obj.level_step.monthly_salary)
    annual_salary = factory.LazyAttribute(
        lambda obj: 12 * obj.level_step.monthly_salary
    )
    event = factory.LazyFunction(lambda: Event.objects.get(id=25))
    wef_date = factory.LazyFunction(lambda: None)
    reason = factory.LazyFunction(lambda: "23% Salary Adjustment")
