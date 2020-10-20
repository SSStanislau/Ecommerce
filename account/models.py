from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Cart

SEX_CHOSEN = [
    ('M', 'Men'),
    ('W', 'Woman'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    sex = models.CharField(choices=SEX_CHOSEN, max_length=1)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class PaymentCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_first_name = models.CharField(max_length=50)
    card_holder_second_name = models.CharField(max_length=50)
    card_expiration_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    card_expiration_year = models.IntegerField(validators=[MinValueValidator(2020)])
    card_cvv = models.CharField(max_length=3)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


def edit_profile(form, user):
    cd = form.cleaned_data
    Profile.objects.filter(user=user).update(
        phone_number=cd['phone_number'],
        sex=cd['sex'],
        address=cd['address']
    )
    User.objects.filter(id=user.id).update(
        first_name=cd['first_name'],
        last_name=cd['last_name'],
        email=cd['email']
    )
