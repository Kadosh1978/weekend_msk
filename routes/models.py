from django.db import models
from django.urls import reverse
from destinations.models import Destination


class Route(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="routes",
        verbose_name="Направление",
    )

    title = models.CharField("Название маршрута", max_length=200)
    slug = models.SlugField("Слаг", unique=True)
    short_description = models.CharField("Короткое описание", max_length=255)

    estimated_time = models.CharField(
        "Ориентировочное время",
        max_length=100,
        blank=True,
    )

    route_includes = models.TextField(
        "Что входит в маршрут",
        blank=True,
    )

    suitable_for = models.TextField(
        "Подходит кому",
        blank=True,
    )

    route_image_1 = models.ImageField(
        "Фото маршрута 1",
        upload_to="routes/",
        blank=True,
        null=True,
    )
    route_image_1_caption = models.CharField(
        "Подпись к фото маршрута 1",
        max_length=255,
        blank=True,
    )

    route_image_2 = models.ImageField(
        "Фото маршрута 2",
        upload_to="routes/",
        blank=True,
        null=True,
    )
    route_image_2_caption = models.CharField(
        "Подпись к фото маршрута 2",
        max_length=255,
        blank=True,
    )

    route_image_3 = models.ImageField(
        "Фото маршрута 3",
        upload_to="routes/",
        blank=True,
        null=True,
    )
    route_image_3_caption = models.CharField(
        "Подпись к фото маршрута 3",
        max_length=255,
        blank=True,
    )

    content = models.TextField("Полный текст", blank=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("routes:detail", kwargs={"slug": self.slug})