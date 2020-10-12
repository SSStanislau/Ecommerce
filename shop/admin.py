from django.utils.html import format_html
from django.contrib import admin
from .models import Product, Category, ProductImage, ShopCollection, Collection, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'available', 'added', 'quantity']
    list_filter = ['available', 'price', 'added']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageAdmin]


class ProductsCollectionAdmin(admin.StackedInline):
    model = Collection


@admin.register(ShopCollection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = [ProductsCollectionAdmin]


@admin.register(ProductReview)
class CategoryAdmin(admin.ModelAdmin):
    pass