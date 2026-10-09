from django.db import models

from constants import MAX_NAME_LENGTH, MAX_SLUG_LENGTH


class Category(models.Model):
    """Модель категории товаров."""
    name = models.CharField(max_length=MAX_NAME_LENGTH, verbose_name='Название',)
    slug = models.SlugField(unique=True, max_length=MAX_SLUG_LENGTH,
                            verbose_name='Идентификатор',)
    image = models.ImageField(upload_to='categories/',
                              verbose_name='Изображение',)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Модель подкатегории товаров."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='subcategories',
                                 verbose_name='Категория',)
    name = models.CharField(max_length=MAX_NAME_LENGTH,
                            verbose_name='Название',)
    slug = models.SlugField(unique=True, max_length=MAX_SLUG_LENGTH,
                            verbose_name='Идентификатор',)
    image = models.ImageField(upload_to='subcategories/',
                              verbose_name='Изображение',)

    class Meta:
        ordering = ('name',)
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.category.name} — {self.name}'
