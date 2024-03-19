from django.contrib.auth.models import User, Group
from django.db import models
from django.contrib.contenttypes.models import ContentType

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    content_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chat(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def has_permission(self, user):
        return user.is_superuser or self.users.filter(pk=user.pk).exists()

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def has_permission(self, user):
        return self.author == user or user.is_superuser

class LogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.content_type} - {self.object_id}"
