from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.base import TemplateView

from shop.models import Product, get_new_collection, get_new_collection_items, Category, ProductReview
from analytics.models import ObjectViewed
from analytics.mixins import ObjectViewMixin


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_collection'] = get_new_collection()
        context['new_collection_items'] = get_new_collection_items()[:5]
        return context


class ProductDetailView(ObjectViewMixin, DetailView):
    model = Product
    queryset = Product.objects.filter(available=True)
    context_object_name = 'item'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        reviews = ProductReview.objects.filter(product=self.get_object())
        context['reviews'] = reviews
        context['reviews_number'] = ProductReview.objects.filter(product=self.get_object()).count()
        if self.request.user.is_authenticated:
            context['last_viewed'] = ObjectViewed.last_five_viewed(self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('text')
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        if request.is_ajax():
            current_product = Product.objects.get(id=product_id)
            new_comment = ProductReview(product=current_product,
                                        body=comment,
                                        owner=self.request.user,
                                        rating=int(rating)
                                        )
            new_comment.save()
            return JsonResponse({'status': 'Ok'})


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
