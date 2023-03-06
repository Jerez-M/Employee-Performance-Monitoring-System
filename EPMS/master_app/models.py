from django.db import models
from datetime import datetime

# Create your models here.

class Organization(models.Model):
    o_name = models.CharField(max_length=100)
    o_email = models.EmailField()
    o_password = models.CharField(max_length=32)
    o_contact = models.CharField(max_length=100)
    o_website = models.CharField(max_length=100)
    o_address = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.o_email} {self.o_password}'

    class Meta:
        db_table = "organization"

class Employee(models.Model):
    o_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    e_name = models.CharField(max_length=100)
    e_email = models.EmailField()
    e_password = models.CharField(max_length=32)
    e_gender = models.CharField(max_length=25)
    e_contact = models.CharField(max_length=100)
    e_address = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.id} {self.e_email} {self.e_password} {self.e_address} {self.e_contact} {self.e_gender}'

    class Meta:
        db_table = "employee"
