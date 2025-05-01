from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .choices import ROLES, DIVISIONS, GRADES


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
        user = self.model(
            fullname=fullname,
            username=username,
            email=email,
            role=role,
            grade=grade,
            division=division,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, fullname, username, email, role, grade, division, password
    ):
        user = self.create_user(
            fullname, username, email, role, grade, division, password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255, blank=False, null=False)
    username = models.CharField(max_length=50, blank=False, null=False, unique=True)
    email = models.CharField(max_length=255, blank=False, null=False, unique=True)
    role = models.CharField(max_length=50, blank=False, null=False, choices=ROLES)
    grade = models.CharField(max_length=50, blank=False, null=False, choices=GRADES)
    division = models.CharField(
        max_length=50, blank=False, null=False, choices=DIVISIONS
    )

    REQUIRED_FIELDS = ["fullname", "email", "role", "grade", "division"]

    objects = UserManager()

    def __str__(self):
        return f"{self.fullname}"
