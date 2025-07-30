import factory
import faker
import factory.django
import random
from courses.models import Courses, InvalidCourseRecords
from employees.models import Employee


fake = faker.Faker()
unique_employees = iter(random.sample(list(Employee.objects.all()), 1500))


class CoursesFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Courses

    employee = factory.LazyFunction(lambda: next(unique_employees))
    course_type = factory.LazyFunction(lambda: f"BSc. Course {random.randint(1,100)}")
    place = factory.LazyFunction(fake.city)
    date_commenced = factory.LazyFunction(fake.date)
    date_ended = factory.LazyFunction(fake.date)
    qualification = factory.LazyAttribute(lambda obj: obj.course_type)
    result = factory.LazyFunction(
        lambda: random.choice(
            ["PASS", "FIRST CLASS HONOURS", "SECOND CLASS UPPER DIVISION"]
        )
    )
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )


class InvalidCourseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = InvalidCourseRecords

    employee = factory.LazyFunction(lambda: next(unique_employees))
    course_type = factory.LazyFunction(lambda: f"BSc. Course {random.randint(1,100)}")
    place = factory.LazyFunction(fake.city)
    date_commenced = factory.LazyFunction(lambda: None)
    date_ended = factory.LazyFunction(lambda: None)
    qualification = factory.LazyAttribute(lambda obj: obj.course_type)
    result = factory.LazyFunction(
        lambda: random.choice(
            ["PASS", "FIRST CLASS HONOURS", "SECOND CLASS UPPER DIVISION"]
        )
    )
    authority = factory.LazyFunction(
        lambda: f"CEM {random.randint(1,50)}/{random.randint(10,25)}"
    )
