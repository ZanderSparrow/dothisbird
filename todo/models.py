from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    # Content of the todo
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)

    # Created at
    created_at = models.DateTimeField(auto_now_add=True)

    # User who owns this todo
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Urgency of this todo
    urgent = models.BooleanField(default=False)

    # Completed boolean
    completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
