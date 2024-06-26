from django.db import models

# Create your models here.


class Place(models.Model):
    title = models.CharField("Заголовок", max_length=200, db_index=True)
    description_short = models.TextField("Короткое описание")
    description_long = models.TextField("Длинное описание")
    latitude = models.FloatField("Широта", blank=True)
    longitude = models.FloatField("Долгота", blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    img = models.ImageField(upload_to='images/', verbose_name="Изображение")
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, verbose_name='Место', related_name='images')
    position = models.IntegerField("Позиция", db_index=True,blank=True)

    def __str__(self):
        return f"{self.position}: {self.place}"

    class Meta:
        ordering = ["position"]
