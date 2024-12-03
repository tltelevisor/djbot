from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    idtlg = models.CharField(max_length=53, null=True, blank=True)
    token = models.CharField(max_length=36, null=True, blank=True)