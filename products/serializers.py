from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='subcategory.category.name',
                                     read_only=True,)
    subcategory = serializers.CharField(source='subcategory.name',
                                        read_only=True,)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'subcategory', 'price', 'images',]

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
