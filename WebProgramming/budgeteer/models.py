from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Account(models.Model):
    """Model for Account object
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateField(auto_now =True)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Model for Transaction object
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    def __str__(self):
        return self.description

class Objective(models.Model):
    """Model for Objective object
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    deadline = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    objective_choices = (
        ('Spend', 'Don\'t spend more than'),
        ('Have', 'Have more than')
    )
    objective = models.CharField(max_length = 5, choices = objective_choices, default = 'Spend')
    name = models.CharField(max_length=256)
    description = models.CharField(max_length = 5)
    completed_choices = (
        ('IP', 'In Progress'),
        ('Y', 'Yes'),
        ('N', 'No')
    )
    completed = models.CharField(max_length = 2, choices = completed_choices, default = 'IP')
    def __str__(self):
        return self.name
