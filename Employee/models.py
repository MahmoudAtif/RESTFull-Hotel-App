from django.db import models
from Hotel.models import AbstractModel
# Create your models here.


class Employee(AbstractModel):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    employee_type = models.ForeignKey(
        'EmployeeType',
        verbose_name=('Type'),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class EmployeeType(AbstractModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
