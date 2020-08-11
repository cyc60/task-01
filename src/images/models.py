import uuid

from django.db import models

from .querysets import ImageQuerySet


class ImageSurface(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class ImageClass(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Image classes"


class Image(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ImageQuerySet.as_manager()


class Annotation(models.Model):
    image = models.OneToOneField(Image, related_name='annotation', on_delete=models.CASCADE)
    meta = models.JSONField(null=True, blank=True)
    image_class = models.ForeignKey(ImageClass, null=True, blank=True, on_delete=models.CASCADE)
    surface = models.ManyToManyField(ImageSurface, blank=True)
    startY = models.FloatField(null=True, blank=True)
    startX = models.FloatField(null=True, blank=True)
    endX = models.FloatField(null=True, blank=True)
    endY = models.FloatField(null=True, blank=True)
