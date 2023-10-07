from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User_dev2(AbstractUser):

    def __str__(self):
        return self.username

    username = models.CharField(max_length=200, unique=True, null=False, blank=False)
    FavIce = models.CharField(max_length=200)
    Shoesize = models.CharField(max_length=200)
    Age = models.CharField(max_length=200)
    Hobbies = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=200)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Specify the field to be used as the username for authentication
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']


class Post(models.Model):
    user = models.ForeignKey(User_dev2, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
