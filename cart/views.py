from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from cart.models import CartItem, Cart
from shop.models import Product
from .cart import SessionsCart


class CartItemsView(ListView):
    model = Cart
    template_name = 'profile/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartItemsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['items'] = Cart.get_items(self.request)
        else:
            context['items'] = SessionsCart(self.request)
        return context


class CreateItemCart(CreateView):
    model = CartItem

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        if request.is_ajax():
            if self.request.user.is_authenticated:
                CartItem.save_to_cart(self.request, product_id)
            else:
                cart = SessionsCart(request)
                product = Product.objects.get(id=product_id)
                cart.add_to_cart(
                    product=product
                )
        return JsonResponse({'status': 'Ok'})
