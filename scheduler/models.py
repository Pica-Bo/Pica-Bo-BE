from django.db import models

# Example model for django-celery-beat custom tasks (optional)
class ExampleTask(models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name
