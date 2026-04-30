from django.db import models
from django.urls import reverse


class Destination(models.Model):
    TRANSPORT_CHOICES = [
        ("train", "Поезд"),
        ("car", "Машина"),
        ("bus", "Автобус"),
        ("plane", "Самолет"),
        ("mixed", "Несколько вариантов"),
    ]

    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Слаг", unique=True)
    short_description = models.CharField("Короткое описание", max_length=255)
    description = models.TextField("Полное описание", blank=True)

    how_to_get = models.TextField("Как добраться", blank=True)
    what_to_see = models.TextField("Что посмотреть", blank=True)
    budget = models.CharField("Бюджет", max_length=255, blank=True)

    days_count = models.CharField("На сколько дней", max_length=100, blank=True)
    transport_type = models.CharField(
        "Лучший транспорт",
        max_length=20,
        choices=TRANSPORT_CHOICES,
        blank=True,
    )

    hero_image = models.ImageField(
        "Hero фото",
        upload_to="destinations/heroes/",
        blank=True,
        null=True,
    )
    hero_image_caption = models.CharField(
        "Подпись к Hero",
        max_length=255,
        blank=True,
        default="",
    )

    gallery_image_1 = models.ImageField(
        "Галерея фото 1",
        upload_to="destinations/gallery/",
        blank=True,
        null=True,
    )
    gallery_image_1_caption = models.CharField(
        "Подпись к фото 1",
        max_length=255,
        blank=True,
        default="",
    )

    gallery_image_2 = models.ImageField(
        "Галерея фото 2",
        upload_to="destinations/gallery/",
        blank=True,
        null=True,
    )
    gallery_image_2_caption = models.CharField(
        "Подпись к фото 2",
        max_length=255,
        blank=True,
        default="",
    )

    gallery_image_3 = models.ImageField(
        "Галерея фото 3",
        upload_to="destinations/gallery/",
        blank=True,
        null=True,
    )
    gallery_image_3_caption = models.CharField(
        "Подпись к фото 3",
        max_length=255,
        blank=True,
        default="",
    )

    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("destinations:detail", kwargs={"slug": self.slug})