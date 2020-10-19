from django.contrib import admin

from cart.models import Cart, CartItem


@admin.register(Cart)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class CategoryAdmin(admin.ModelAdmin):
    pass