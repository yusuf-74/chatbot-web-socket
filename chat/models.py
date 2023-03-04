from django.db import models


class Message(models.Model):
    text = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'auth.User', related_name='messages', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('createdAt',)

class Response(models.Model):
    text = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    message = models.OneToOneField(
        Message, related_name='response',on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('createdAt',)