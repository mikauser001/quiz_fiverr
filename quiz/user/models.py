from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Fügen Sie hier weitere benutzerdefinierte Felder hinzu, wenn erforderlich
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    is_mod = models.BooleanField(default=False)

    def reset(self):
        self.points, self.rank = 0, 0
        self.save(update_fields=["points", "rank"])

