from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from cart.models import CartItem, Cart


class CartItemsView(ListView):
    model = Cart
    template_name = 'profile/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartItemsView, self).get_context_data(**kwargs)
        context['items'] = Cart.get_items(self.request)
        return context


class CreateItemCart(CreateView):
    model = CartItem

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        if request.is_ajax():
            CartItem.save_to_cart(self.request, product_id)
            return JsonResponse({'status': 'Ok'})