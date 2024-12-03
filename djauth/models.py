from django.db import models
from django.contrib.auth.models import AbstractUser
# Два дополнительных поля для пользователей Telegram 
class User(AbstractUser):
    # id поьзователя Telegram
    idtlg = models.CharField(max_length=53, null=True, blank=True)
    # Токен. По этому полю будет устанавливаться соответствие пользователя, 
    # получившего форму от Django и пользователя Telegram, отрпавившего сообщение в бот
    token = models.CharField(max_length=36, null=True, blank=True)
    # Оба эти поля можно было бы хранить в каких-нибудь полях типа last_name, 
    # не нарушая стандартную базу данных. Такой "костыль" может пригодиться для существующих баз.