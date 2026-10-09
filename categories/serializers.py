from rest_framework import serializers

from .models import Category, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории."""
    id = serializers.IntegerField(label='Идентификатор пользователя',
                                  read_only=True)
    name = serializers.CharField(label='Название')
    slug = serializers.SlugField(label='Идентификатор')
    image = serializers.ImageField(label='Изображение')

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'slug', 'image']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""
    id = serializers.IntegerField(label='Идентификатор пользователя',
                                  read_only=True)
    name = serializers.CharField(label='Название')
    slug = serializers.SlugField(label='Идентификатор')
    image = serializers.ImageField(label='Изображение')
    subcategories = SubcategorySerializer(many=True, read_only=True,
                                          label='Подкатегории',)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategories',]
