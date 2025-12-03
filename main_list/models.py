from django.db import models

# Create your models here.
class Person(models.Model):
    person_enum = [
        ('Mom', 'Mom'),
        ('Dad', 'Dad'),
        ('Court', 'Court'),
        ('Andrew', 'Andrew'),
        ('Eliza', 'Eliza'),
        ('Maggie', 'Maggie'),
        ('Hannah', 'Hannah')
    ]

    who = models.CharField(max_length=200, choices=person_enum)



class Item(models.Model):
    type_gift_enum = [
        ("stocking", "Stocking"),
        ("main", "Main")
    ]

    name = models.CharField(max_length=200)
    who = models.ManyToManyField(Person, blank=True)
    type_gift = models.CharField(max_length=20, choices=type_gift_enum)
    price=models.FloatField()