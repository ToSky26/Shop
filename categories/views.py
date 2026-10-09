from rest_framework.generics import ListAPIView

from .models import Category
from .serializers import CategorySerializer


class CategoryListAPIView(ListAPIView):
    """Возвращение списка категорий с вложенными подкатегориями."""
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
