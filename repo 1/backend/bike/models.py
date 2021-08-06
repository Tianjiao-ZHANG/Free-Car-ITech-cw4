from django.db import models

# Create your models here.
class bike(models.Model):
    iid = models.CharField(max_length=8)
    brand = models.CharField(max_length=20)
    price = models.FloatField(default=1.0)
    avaliable = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.iid, self.brand

class user(models.Model):
    username = models.CharField(max_length=8)
    password = models.CharField(max_length=20)
    mail = models.CharField(max_length=20)
    balance = models.FloatField()
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.username