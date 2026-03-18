from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

class User(AbstractUser):
    last_seen = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(unique=True)
    status = models.BooleanField(default=False)
    def is_online(self):
        if self.last_seen:
            return timezone.now() - self.last_seen < timedelta(minutes=5)
        return False

class Chat(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="messages/files/", blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:30] if self.content else "File message"




class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, blank=True)  # имя, которое пользователь сам указал
    age = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.display_name or self.user.username