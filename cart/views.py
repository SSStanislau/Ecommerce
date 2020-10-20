from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
            context['total_price'] = Cart.get_total_price(self.request)
        else:
            cart = SessionsCart(self.request)
            context['items'] = cart
            context['total_price'] = cart.get_total_price()
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


class DeleteItemFromCart(DeleteView):
    model = CartItem

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteItemFromCart, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('id')
        product_id = request.POST.get('product_id')
        if request.is_ajax():
            if self.request.user.is_authenticated:
                CartItem.delete_item(item_id)
            else:
                cart = SessionsCart(request)
                product = Product.objects.get(id=product_id)
                cart.remove(
                    product=product
                )
        return JsonResponse({'status': 'Ok'})