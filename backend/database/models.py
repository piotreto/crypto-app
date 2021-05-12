from django.db import models
from email_validator import DOMAIN_MAX_LENGTH

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=50)
    dollars = models.FloatField(default=0)

    def __str__(self):
        return str(self.email) + " " + str(self.password)

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptoID = models.CharField(max_length=40)
    amount = models.FloatField(default=0)
