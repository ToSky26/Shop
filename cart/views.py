from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem
from .serializers import CartItemSerializer, CartItemWriteSerializer


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user).select_related(
            'product', 'product__subcategory', 'product__subcategory__category',
        )

        total_quantity = sum(item.quantity for item in items)
        total_price = sum(
            (item.product.price * item.quantity
             for item in items), Decimal('0.00'),
        )

        return Response({
            'items': CartItemSerializer(
                items, many=True, context={'request': request},
            ).data, 'total_quantity': total_quantity,
            'total_price': total_price,
        })

    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartItemWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item, created = CartItem.objects.get_or_create(
            user=request.user, product=serializer.validated_data['product'],
            defaults={'quantity': serializer.validated_data['quantity'], },)

        if not created:
            item.quantity += serializer.validated_data['quantity']
            item.save(update_fields=['quantity'])

        return Response(
            CartItemSerializer(item).data, status=status.HTTP_201_CREATED,
        )

    def patch(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, user=request.user,)
        serializer = CartItemWriteSerializer(item, data=request.data,
                                             partial=True,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CartItemSerializer(item).data)

    def delete(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, user=request.user,)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
