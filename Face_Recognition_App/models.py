from django.db import models
import json

# Create your models here.

class Person(models.Model):
    Name_encoding = models.TextField()
    Name = models.CharField(max_length=50)

    def __str__(self):
        return self.Name
        

class Detected_person(models.Model):
    Name = models.CharField(max_length=50)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)

