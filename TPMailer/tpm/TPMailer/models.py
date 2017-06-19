from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

# Create your models here.

class Confirmation(models.Model):
    msg_txt = models.CharField(max_length=32)
    gen_date = models.DateTimeField(default=timezone.now)
    is_checked = models.BooleanField(default=False)

    objects = models.Manager()  # Default Manager

    def __str__(self):
        return self.msg_txt

    def new_con():
        con = Confirmation()
        con.msg_txt = get_random_string(length=32,
                                        allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        con.save()
        return con.pk


class User(AbstractUser):
    email = models.EmailField(unique=True)
    confirmation = models.ForeignKey(Confirmation,
                                     on_delete=None,
                                     related_name="tpmailers_user_related",
                                     related_query_name="tpmailers_user",
                                     default=Confirmation.new_con())

    REQUIRED_FIELDS = ('first_name', 'last_name', 'username', 'password')

    USERNAME_FIELD = 'email'




