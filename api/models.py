from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Profile(models.Model):
    username = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=500, default="", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profilepic = models.ImageField(upload_to="uploads/users/", default="uploads/users/default.png")

class Post(models.Model):
    text = models.CharField(max_length=500)
    image = models.ImageField(upload_to="uploads/posts/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
