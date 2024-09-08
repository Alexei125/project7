from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город проживания",
        help_text="Укажите город проживания",
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        default="users/avatars/default_avatar.png",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    date_of_pyment = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    payment_status = models.CharField(max_length=50, verbose_name="Статус оплаты")
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    method = models.CharField(max_length=5, verbose_name="Способ оплаты")
    session_id = models.CharField(
        max_length=200, verbose_name="Id сессии", blank=True, null=True
    )
    link = models.URLField(max_length=400, verbose_name="Ссылка", blank=True, null=True)
    user - models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
        related_name="payments",
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"{self.user} - {self.date_of_pyment}"
