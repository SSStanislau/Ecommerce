from django.contrib import admin

from account.models import Profile, PaymentCard


@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentCard)
class CategoryAdmin(admin.ModelAdmin):
    pass
