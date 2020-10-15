from django.contrib import admin

from .models import ObjectViewed, UserSession


@admin.register(ObjectViewed)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSession)
class CategoryAdmin(admin.ModelAdmin):
    pass
