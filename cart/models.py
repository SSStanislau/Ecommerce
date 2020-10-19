from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from shop.models import Product


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('cart:cart', args=[self.id])

    @classmethod
    def get_items(cls, request):
        cart = cls.objects.get(owner=request.user.id)
        return CartItem.objects.filter(cart=cart)


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
