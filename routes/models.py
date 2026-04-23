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