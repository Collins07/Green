
from datetime import date
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Forest(models.Model):
    trees_planted = models.IntegerField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    reason = models.CharField( max_length=256)

    def __str__(self):
        return self.reason
    
    class Meta:
        ordering: list['-date']
        



class Reason(models.Model):
        name = models.CharField(max_length=250)


        def __str__(self):
             return self.name



