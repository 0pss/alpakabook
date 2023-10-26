from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.


class User_dev2(AbstractUser):

    def __str__(self):
        return self.anzeigename

    anzeigename = models.CharField(max_length=200, null=False, blank=False)
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

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    # Specify the field to be used as the username for authentication
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']


class Post(models.Model):
    user = models.ForeignKey(User_dev2, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=False, editable=True, default=timezone.now())


from django.contrib.auth.models import User
from django.db import models

class Friendship(models.Model):
    sender = models.ForeignKey(User_dev2, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User_dev2, related_name='received_friend_requests', on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('send_request', 'Freundschaftsanfrage schicken'),
        ('request_sent', 'Anfrage verschickt'),
        ('friends', 'Befreundet'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='send_request')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['sender', 'receiver']


from django.contrib.auth.models import User
from django.db import models

class Notification(models.Model):
    sender = models.ForeignKey(User_dev2, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(User_dev2, on_delete=models.CASCADE, related_name='received_notifications')
    notification_type = models.CharField(max_length=20)  # E.g., 'friend_request'
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)