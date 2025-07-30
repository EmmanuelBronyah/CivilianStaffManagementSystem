import factory
import faker
import factory.django
from employees import models
import random
from marriage.models import Spouse


fake = faker.Faker()
unique_employees = iter(random.sample(list(models.Employee.objects.all()), 500))


class MarriageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Spouse

    employee = factory.LazyFunction(lambda: next(unique_employees))
    spouse_name = factory.LazyAttribute(
        lambda obj: (
            fake.name_female()
            if obj.employee.gender.sex.lower() == "male"
            else fake.name_male()
        )
    )
    phone_number = factory.LazyFunction(fake.phone_number)
    address = factory.LazyFunction(fake.address)
    registration_number = factory.LazyFunction(
        lambda: "".join(fake.random_letters(length=13))
    )
    marriage_date = factory.LazyFunction(fake.date)
    marriage_place = factory.LazyFunction(fake.city)
