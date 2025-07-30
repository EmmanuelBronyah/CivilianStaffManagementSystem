import factory
import faker
import factory.django
from employees.models import Employee
import random
from identity.models import Identity


fake = faker.Faker()
unique_employees = iter(random.sample(list(Employee.objects.all()), 500))


class IdentityFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Identity

    employee = factory.LazyFunction(lambda: next(unique_employees))
    voters_id = factory.LazyFunction(lambda: "".join(fake.random_letters(length=13)))
    national_id = factory.LazyFunction(lambda: "".join(fake.random_letters(length=13)))
    glico_id = factory.LazyFunction(lambda: "".join(fake.random_letters(length=13)))
    nhis_id = factory.LazyFunction(lambda: "".join(fake.random_letters(length=13)))
    tin_number = factory.LazyFunction(lambda: "".join(fake.random_letters(length=13)))
