from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    person_enum = [
        ('Mom', 'Mom'),
        ('Dad', 'Dad'),
        ('Court', 'Court'),
        ('Andrew', 'Andrew'),
        ("Ben", "Ben"),
        ('Eliza', 'Eliza'),
        ('Maggie', 'Maggie'),
        ("Phinney", "Phinney"),
        ('Secret santa', 'Secret santa')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    who = models.CharField(max_length=200, choices=person_enum)

    def __str__(self):
        return self.who



class Item(models.Model):
    type_gift_enum = [
        ("stocking", "Stocking"),
        ("main", "Main")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    who = models.ManyToManyField(Person, blank=True)
    type_gift = models.CharField(max_length=20, choices=type_gift_enum)
    price = models.FloatField()