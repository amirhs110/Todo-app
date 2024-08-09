from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_snippet(self):
        words = self.content.split()
        snippet = " ".join(words[:5])
        if len(words) > 5:
            snippet += "..."
        return snippet

    def get_absolute_url(self):
        return reverse("task:api-v1:task-detail", kwargs={"pk": self.pk})

    def get_task_url(self):
        url = reverse("task:api-v1:task-detail", kwargs={"pk": self.pk})
        url = "http://127.0.0.1:8000" + url
        return url
