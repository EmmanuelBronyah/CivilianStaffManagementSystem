from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import logging
from employees.models import Grades


logger = logging.getLogger(__name__)


ROLES = [
    ("ADMINISTRATOR", "Administrator"),
    ("STANDARD USER", "Standard User"),
    ("VIEWER", "Viewer"),
]


class UserManager(BaseUserManager):

    def create_user(self, fullname, username, email, role, grade, division, password):
        if not fullname:
            raise ValueError("User must have a full name.")
        if not username:
            raise ValueError("User must have a username.")
        if not email:
            raise ValueError("User must have an email.")
        if not role:
            raise ValueError("User must have a role.")
        if not grade:
            raise ValueError("User must have a grade.")
        if not division:
            raise ValueError("User must have a division.")
        if not password:
            raise ValueError("User must have a password.")

        email = self.normalize_email(email)
        logger.debug("User email has been set.")

        if isinstance(grade, int):
            grade = Grades.objects.get(pk=grade)
        if isinstance(division, int):
            division = Divisions.objects.get(pk=division)

        user = self.model(
            fullname=fullname,
            username=username,
            email=email,
            role=role,
            grade=grade,
            division=division,
        )
        user.set_password(password)
        logger.debug("User password has been set.")
        user.save(using=self._db)
        logger.debug(f"User({user}) saved to database.")

        return user

    def create_superuser(
        self, fullname, username, email, role, grade, division, password
    ):
        user = self.create_user(
            fullname, username, email, role, grade, division, password
        )
        logger.debug("Superuser user instance has been created.")
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        logger.debug(f"Superuser({user}) saved to database.")

        return user


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=50, choices=ROLES)
    grade = models.ForeignKey(Grades, on_delete=models.PROTECT)
    division = models.ForeignKey("Divisions", on_delete=models.PROTECT)

    REQUIRED_FIELDS = ["fullname", "email", "role", "grade", "division"]

    objects = UserManager()

    class Meta:
        db_table = "Users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.fullname}"


class Divisions(models.Model):
    division = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "Divisions"
        verbose_name = "Division"
        verbose_name_plural = "Divisions"

    def __str__(self):
        return f"{self.division}"
