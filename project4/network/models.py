from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "posterUsername": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        }

class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    userFollower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userFollower")
    followingStatus = models.BooleanField(default=False)

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    likeStatus = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)