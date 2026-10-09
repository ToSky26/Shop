from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CartItem
from .serializers import CartItemSerializer, CartItemWriteSerializer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        items = CartItem.objects.filter(user=request.user).select_related(
            'product', 'product__subcategory',
            'product__subcategory__category',
        )
        total_quantity = sum(item.quantity for item in items)
        total_price = sum(
            (item.product.price * item.quantity for item in items),
            Decimal('0.00'),
        )
        return Response({'items': CartItemSerializer(
            items, many=True, context={'request': request},
            ).data, 'total_quantity': total_quantity,
            'total_price': total_price, })

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='items')
    def add_item(self, request):
        serializer = CartItemWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item, created = CartItem.objects.get_or_create(
            user=request.user, product=serializer.validated_data['product'],
            defaults={'quantity': serializer.validated_data['quantity'], },
        )

        if not created:
            item.quantity += serializer.validated_data['quantity']
            item.save(update_fields=['quantity'])

        return Response(CartItemSerializer(item).data,
                        status=status.HTTP_201_CREATED,)

    @action(detail=True, methods=['patch'], url_path='items')
    def update_item(self, request, pk=None):
        item = get_object_or_404(CartItem, pk=pk, user=request.user,)
        serializer = CartItemWriteSerializer(item, data=request.data,
                                             partial=True,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CartItemSerializer(item).data)

    @action(detail=True, methods=['delete'], url_path='items')
    def remove_item(self, request, pk=None):
        item = get_object_or_404(CartItem, pk=pk, user=request.user,)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
