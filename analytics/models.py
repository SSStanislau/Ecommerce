from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.sessions.models import Session

from account.signals import user_logged_in
from analytics.signals import object_viewed_signal
from analytics.utils import get_client_ip
from shop.models import Product

User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(ContentType, models.CASCADE)
    object_id = models.PositiveIntegerField()
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return f"{self.content_object} viewed: {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

    @classmethod
    def last_five_viewed(cls, user):
        last_viewed = cls.objects.filter(user=user).order_by('object_id').distinct('object_id')[:5]
        return [Product.objects.get(id=item.object_id) for item in last_viewed]


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    ip_address = None
    try:
        ip_address = get_client_ip(request)
    except:
        pass
    ObjectViewed.objects.create(
        user=request.user,
        content_type=c_type,
        object_id=instance.id,
        ip_address=ip_address
    )


object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=120, blank=True, null=True)
    session_key = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def user_logged_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in.connect(user_logged_receiver)


