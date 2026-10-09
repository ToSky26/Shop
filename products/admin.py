from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subcategory', 'price', 'slug',)
    search_fields = ('name', 'slug')
    list_filter = ('subcategory',)
