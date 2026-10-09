from rest_framework import serializers

from products.serializers import ProductSerializer

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        read_only_fields = fields

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
        extra_kwargs = {'quantity': {'min_value': 1}, }
