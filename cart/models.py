from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from shop.models import Product


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_items(cls, request):
        cart = cls.objects.get(owner=request.user.id)
        return CartItem.objects.filter(cart=cart)

    @classmethod
    def get_total_price(cls, request):
        cart = cart = cls.objects.get(owner=request.user.id)
        cart_items = CartItem.objects.filter(cart=cart)
        return sum([item.product.price for item in cart_items])


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    @classmethod
    def save_to_cart(cls, request, product_id):
        user = request.user
        cart = Cart.objects.get(owner=user)
        product = Product.objects.get(id=product_id)
        cls(
            product=product,
            cart=cart
        ).save()

    @classmethod
    def delete_item(cls, cart_item):
        item = cls.objects.get(id=cart_item).delete()
