from django.db import models
from django.utils import timezone
from apps.core.models import User


class Health(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep = models.PositiveIntegerField(default=0)
    steps = models.PositiveIntegerField(default=0)
    water = models.PositiveIntegerField(default=0)
    date = models.DateField(default=timezone.now)
