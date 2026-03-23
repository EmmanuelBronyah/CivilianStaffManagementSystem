import factory
import faker
import factory.django
from employees.models import Employee
import random
from occurance.models import Occurrence, LevelStep, Event, IncompleteOccurrence


fake = faker.Faker()
unique_employees = iter(random.sample(list(Employee.objects.all()), 19000))
EMPLOYEES = list(Employee.objects.all())
LEVELSTEP = list(LevelStep.objects.all())


class OccurrenceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Occurrence

    employee = factory.Iterator(EMPLOYEES)
    grade = factory.LazyAttribute(lambda obj: obj.employee.grade)
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
    level_step = factory.LazyFunction(lambda: random.choice(LEVELSTEP))
    monthly_salary = factory.LazyAttribute(lambda obj: obj.level_step.monthly_salary)
    annual_salary = factory.LazyAttribute(
        lambda obj: 12 * obj.level_step.monthly_salary
    )
    event = factory.LazyFunction(lambda: Event.objects.get(id=2))
    wef_date = factory.LazyFunction(fake.date)
    reason = factory.LazyFunction(lambda: "Newly Employed")


def get_level_step(obj):
    occurrences = obj.employee.occurrences.all()

    if occurrences:
        return occurrences[0].level_step
    else:
        return LevelStep.objects.get(id=1)


class IncompleteOccurrenceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = IncompleteOccurrence

    employee = factory.LazyFunction(lambda: next(unique_employees))
    grade = factory.LazyAttribute(lambda obj: obj.employee.grade)
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
    level_step = factory.LazyAttribute(lambda obj: get_level_step(obj))
    monthly_salary = factory.LazyAttribute(lambda obj: obj.level_step.monthly_salary)
    annual_salary = factory.LazyAttribute(
        lambda obj: 12 * obj.level_step.monthly_salary
    )
    event = factory.LazyFunction(lambda: Event.objects.get(id=1))
    wef_date = factory.LazyFunction(lambda: None)
    reason = factory.LazyFunction(lambda: "23% Salary Adjustment")
