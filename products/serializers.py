from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товара."""
    name = serializers.CharField(label='Название', read_only=True)
    slug = serializers.SlugField(label='Идентификатор', read_only=True,)
    category = serializers.CharField(source='subcategory.category.name',
                                     read_only=True, label='Категория',)
    subcategory = serializers.CharField(source='subcategory.name',
                                        read_only=True, label='Подкатегория',)
    images = serializers.SerializerMethodField(label='Изображения',)
    price = serializers.DecimalField(max_digits=10, decimal_places=2,
                                     label='Цена', read_only=True,)

    class Meta:
        model = Product
        fields = ['name', 'slug', 'category',
                  'subcategory', 'price', 'images',]

    def get_images(self, obj):
        return [
            image.url
            for image in (
                obj.image_small,
                obj.image_medium,
                obj.image_large,
            )
            if image
        ]
