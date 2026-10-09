from django.db import models

from categories.models import Subcategory
from constants import MAX_NAME_LENGTH, MAX_SLUG_LENGTH


class Product(models.Model):
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name='products',
        verbose_name='Подкатегория',
    )
    name = models.CharField(max_length=MAX_NAME_LENGTH, verbose_name='Название',)
    slug = models.SlugField(unique=True, max_length=MAX_SLUG_LENGTH,
                            verbose_name='Идентификатор',)
    image_small = models.ImageField(upload_to='products/',
                                    verbose_name='Маленькое изображение',)
    image_medium = models.ImageField(upload_to='products/',
                                     verbose_name='Среднее изображение',)
    image_large = models.ImageField(upload_to='products/',
                                    verbose_name='Большое изображение',)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена',)

    class Meta:
        ordering = ('name',)
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
