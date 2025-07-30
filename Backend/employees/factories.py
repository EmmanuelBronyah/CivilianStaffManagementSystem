import factory
import faker
import factory.django
from employees import models
import random


fake = faker.Faker()
unique_ids = iter(random.sample(range(10000, 30001), 20000))
unique_employees = iter(random.sample(list(models.Employee.objects.all()), 500))


class EmployeeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Employee

    service_id = factory.LazyFunction(lambda: "0" + str(next(unique_ids)))
    gender = factory.LazyFunction(
        lambda: random.choice(list(models.Gender.objects.all()))
    )
    lastname = factory.LazyAttribute(
        lambda obj: (
            fake.last_name_male()
            if obj.gender.sex.lower() == "male"
            else fake.last_name_female()
        )
    )
    other_names = factory.LazyAttribute(
        lambda obj: (
            fake.first_name_male()
            if obj.gender.sex.lower() == "male"
            else fake.first_name_female()
        )
    )
    dob = factory.LazyFunction(
        lambda: fake.date_of_birth(minimum_age=18, maximum_age=65)
    )
    hometown = factory.LazyFunction(lambda: f"{fake.city()} - {fake.state()}")
    region = factory.Iterator(models.Region.objects.all())
    religion = factory.Iterator(models.Religion.objects.all())
    nationality = factory.LazyFunction(
        lambda: random.choice(["GHANAIAN", "NIGERIAN", "IVORIAN"])
    )
    address = factory.LazyFunction(fake.address)
    email = factory.LazyFunction(fake.email)
    marital_status = factory.Iterator(models.MaritalStatus.objects.all())
    unit = factory.Iterator(models.Units.objects.all())
    grade = factory.Iterator(models.Grades.objects.all())
    station = factory.LazyFunction(fake.state)
    structure = factory.Iterator(models.Structure.objects.all())
    blood_group = factory.Iterator(models.BloodGroup.objects.all())
    disable = factory.LazyFunction(lambda: fake.boolean(chance_of_getting_true=5))
    social_security = factory.LazyFunction(
        lambda: "".join(fake.random_letters(length=13))
    )
    category = factory.LazyFunction(lambda: random.choice(["Senior", "Junior"]))
    appointment_date = factory.LazyFunction(fake.date)
    confirmation_date = factory.LazyFunction(fake.date)
    probation = factory.LazyFunction(lambda: str(random.randint(1, 3)))
    entry_qualification = factory.LazyFunction(
        lambda: "".join(fake.random_letters(length=13))
    )


class UnregisteredEmployeesFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.UnregisteredEmployees

    service_id = factory.LazyFunction(lambda: None)
    last_name = factory.LazyFunction(lambda: fake.last_name())
    other_names = factory.LazyFunction(lambda: fake.first_name())
    unit = factory.LazyFunction(lambda: random.choice(models.Units.objects.all()))
    grade = factory.LazyFunction(lambda: None)
    social_security = factory.LazyFunction(lambda: None)
