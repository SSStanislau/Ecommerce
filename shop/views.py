from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.base import TemplateView

from shop.models import Product, get_new_collection, get_new_collection_items, ShopCollection, Category, ProductReview


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_collection'] = get_new_collection()
        context['new_collection_items'] = get_new_collection_items()[:5]
        return context


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.filter(available=True)
    context_object_name = 'item'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        reviews = ProductReview.objects.filter(product=self.get_object())
        context['reviews'] = reviews
        context['reviews_number'] = ProductReview.objects.filter(product=self.get_object()).count()
        return context


class ShopListView(CreateView):
    model = Category
    template_name = 'shop_index.html'

    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return render(request,
                      self.template_name,
                      {'category': category,
                       'categories': categories,
                       'products': products}
                      )
