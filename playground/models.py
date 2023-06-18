from django.db import models

# Create your models here.
class User_dev(models.Model):

    def __str__(self):
            return self.Name

    Name = models.CharField(max_length=200)
    Email = models.CharField(max_length=200)
    FavIce = models.CharField(max_length=200)
    Shoesize = models.CharField(max_length=200)
    Age = models.CharField(max_length=200)
    Hobbies = models.CharField(max_length=200)
    created_date = models.DateTimeField("date published")

