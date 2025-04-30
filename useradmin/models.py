from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Estos campos ya están incluidos en AbstractUser:
    # username, first_name, last_name, email, password, etc.
    
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campos adicionales si son necesarios

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Create your models here.
