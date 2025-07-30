import factory
import faker
import factory.django
from employees.models import Employee
import random
from next_of_kin.models import EmergencyOrNextOfKin


fake = faker.Faker()


class EmergencyOrNextOfKinFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EmergencyOrNextOfKin

    employee = factory.Iterator(Employee.objects.all())
    name = factory.LazyFunction(fake.name)
    relation = factory.LazyFunction(
        lambda: random.choice(["Sister", "Brother", "Niece", "Nephew"])
    )
    email = factory.LazyFunction(fake.email)
    address = factory.LazyFunction(fake.address)
    phone_number = factory.LazyFunction(fake.phone_number)
    emergency_contact = factory.LazyFunction(fake.phone_number)
