from django.urls import path

from .views import CartAPIView, CartItemAPIView

urlpatterns = [
    path('', CartAPIView.as_view(), name='cart'),
    path('items/', CartItemAPIView.as_view(), name='cart-item-create'),
    path('items/[int:pk](int:pk)/', CartItemAPIView.as_view(),
         name='cart-item-detail',),
]
