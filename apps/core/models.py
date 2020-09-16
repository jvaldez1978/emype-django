from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    foto = models.ImageField(upload_to='usrs/fotos', null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None

