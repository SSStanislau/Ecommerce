from django.urls import path

from cart.views import CartItemsView, CreateItemCart, DeleteItemFromCart

app_name = 'cart'

urlpatterns = [
    path('', CartItemsView.as_view(), name='cart'),
    path('add/<int:product>', CreateItemCart.as_view(), name='add_to_cart'),
    path('remove/<int:product>', DeleteItemFromCart.as_view(), name='remove_from_cart')
]
