from django.contrib import admin
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from .models import Place, Image

from django.db import models

class ImageInline( admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ["preview_image"]

    @staticmethod
    def preview_image(obj):
        if obj.img:
            return format_html('<img src="{url}" style="max-height: 200px; max-width: 200px;" />',
                           url=obj.img.url)
        return format_html('<p>Здесь будет превью, когда вы выберете файл</p>')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]
    formfield_overrides = {
            models.TextField: {'widget': TinyMCE()},
        } 
    search_fields = ['title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ["preview_image"]
    raw_id_fields = ["place", ]
    autocomplete_fields = ["place"]

    @staticmethod
    def preview_image(obj): 
        if obj.img:
            return format_html('<img src="{url}" height=200px/>',
                               url=obj.img.url)
        return format_html(
            '<p>Здесь будет превью, когда вы создадите изображение</p>')