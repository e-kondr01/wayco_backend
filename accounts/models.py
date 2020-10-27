from django.db import models
from django.contrib.auth.models import User

from common.models import Cafe


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_cafes = models.ManyToManyField(Cafe)

    def __str__(self) -> str:
        return f'{self.user}'
