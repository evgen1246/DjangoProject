from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True,verbose_name='Имя пользователя',blank=True,null=True,)
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите электронную почту")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name="Введите номер телефона", blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name="Введите название страны", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email



