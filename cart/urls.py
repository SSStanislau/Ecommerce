from django.urls import path

from cart.views import CartItemsView, CreateItemCart

app_name = 'cart'

urlpatterns = [
    path('cart/<int:id>', CartItemsView.as_view(), name='cart'),
    path('cart/add', CreateItemCart.as_view(), name='add_to_cart')
]
