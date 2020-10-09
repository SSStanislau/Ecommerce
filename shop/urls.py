from django.urls import path

from shop.views import HomePageView, ProductDetailView, ShopListView

app_name = 'shop'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('shop/<str:category>/<slug:slug>/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('shop', ShopListView.as_view(), name='shop'),
    path('shop/<slug:category_slug>/', ShopListView.as_view(), name='product_list_by_category')
]