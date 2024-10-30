from django.db import models

# Create your models here.


class Member (models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    username = models.CharField(null=True, max_length=255)
    join_date = models.DateField(null=True)


    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def initials(self):
        return f"{self.firstname[0]}{self.lastname[0]}".upper()