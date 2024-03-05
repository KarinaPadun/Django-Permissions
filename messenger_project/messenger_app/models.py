from django.contrib.auth.models import User, Group

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
