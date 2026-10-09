from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название',)
    slug = models.SlugField(unique=True, max_length=170,
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='subcategories',
                                 verbose_name='Категория',)
    name = models.CharField(max_length=150, verbose_name='Название',)
    slug = models.SlugField(unique=True, max_length=170,
                            verbose_name='Идентификатор',)
    image = models.ImageField(upload_to='subcategories/',
                              verbose_name='Изображение',)

    class Meta:
        ordering = ('name',)
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.category.name} — {self.name}'
