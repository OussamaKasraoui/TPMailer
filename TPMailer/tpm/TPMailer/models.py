from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.

class Confirmation(models.Model):
    msg_txt = models.CharField(max_length=32)
    gen_date = models.DateTimeField(default=timezone.now)
    is_checked = models.BooleanField(default=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = models.Manager()  # Default Manager

    def __str__(self):
        return self.msg_txt

# Subclass Def User for any coming extends
class User(AbstractUser, UserManager):
    email = models.EmailField(unique=True, blank=False)

    USERNAME_FIELD = 'username'
    pass