from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.db.models import Avg


class ShopEntityModel(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(ShopEntityModel):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(ShopEntityModel):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    added = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=30)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-added',)
        index_together = ('id', 'slug')

    @property
    def product_cover(self):
        return ProductImage.objects.filter(product=self.id)[0].image

    @property
    def product_images(self):
        return ProductImage.objects.filter(product=self.id)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       kwargs={'category': self.category,
                               'slug': self.slug,
                               'pk': self.id})

    def get_avg_rating(self):
        reviews = ProductReview.objects.filter(product=self.id)
        if reviews:
            return int(reviews.aggregate(Avg('rating'))['rating__avg'])
        return 0


class ProductEntityModel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)

    class Meta:
        abstract = True


class ProductImage(ProductEntityModel):
    image = models.ImageField(upload_to='products/', null=True, blank=True)


class ShopCollection(ShopEntityModel):
    available = models.BooleanField(default=True)
    timestamp = models.DateField(auto_now_add=True)
    cover = models.ImageField(upload_to='collections/', blank=True)


class Collection(ProductEntityModel):
    collection = models.ForeignKey(ShopCollection, on_delete=models.CASCADE)


def get_new_collection():
    return ShopCollection.objects.filter(available=True).order_by('-timestamp')[0]


def get_new_collection_items():
    return Collection.objects.filter(collection=get_new_collection().id)


class ProductReview(ProductEntityModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(validators=[MaxValueValidator(2020)])
    body = models.CharField(max_length=255)

    class Meta:
        ordering = ('-timestamp',)
