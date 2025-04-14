from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


ROLES = [
  ("ADMINISTRATOR", "Administrator"),
  ("STANDARD USER", "Standard User"),
  ("VIEWER", "Viewer"),
]


class UserManager(BaseUserManager):
  
  def create_user(self, full_name, username, email, role, password):
    if not full_name:
      raise ValueError("User must have a full name.")
    if not username:
      raise ValueError("User must have a username.")
    if not email:
      raise ValueError("User must have an email.")
    if not role:
      raise ValueError("User must have a role.")
    if not password:
      raise ValueError("User must have a password.")
    
    email = self.normalize_email(email)
    user = self.model(full_name=full_name, username=username, email=email, role=role)
    user.set_password(password)
    user.save(using=self._db)
    
    return user

  def create_superuser(self, full_name, username, email, role, password):
    user = self.create_user(full_name, username, email, role, password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    
    return user
  
 
class CustomUser(AbstractUser):
  full_name = models.CharField(max_length=255, blank=False, null=False)
  username = models.CharField(max_length=50, blank=False, null=False, unique=True)
  email = models.CharField(max_length=255, blank=False, null=False, unique=True)
  role = models.CharField(max_length=50, blank=False, null=False, choices=ROLES)
  
  REQUIRED_FIELDS = ["full_name", "email", "role"]

  objects = UserManager()
  
  def __str__(self):
    return f'{self.full_name}'
