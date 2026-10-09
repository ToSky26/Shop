from django.conf import settings
from django.db import models

from products.models import Product


class CartItem(models.Model):
    """Модель корзины пользователя."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='cart_items', verbose_name='Пользователь',
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Товар',)
    quantity = models.PositiveIntegerField(default=1,
                                           verbose_name='Количество',)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'],
                                    name='unique_user_cart_product',)
        ]
        verbose_name = 'товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        """Возвращение названия товара и его количество."""
        return f'{self.product.name} — {self.quantity}'
