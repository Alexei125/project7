from django.db import models

from config import settings
from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    image = models.ImageField(
        upload_to="materials/course/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Добавьте изображение",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Владелец курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name="lessons",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )

    image = models.ImageField(
        upload_to="materials/lesson/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Добавьте изображение",
    )

    link_to_video = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='курс')
    is_subscribe = models.BooleanField(default=False, verbose_name="подписка")

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'