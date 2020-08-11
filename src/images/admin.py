from django.contrib import admin

from .models import Image, Annotation, ImageClass, ImageSurface


class AnnotationInline(admin.StackedInline):
    model = Annotation


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    inlines = [AnnotationInline]


@admin.register(ImageSurface)
class ImageSurfaceAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageClass)
class ImageClassAdmin(admin.ModelAdmin):
    pass
