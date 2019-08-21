from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save



User = settings.AUTH_USER_MODEL


class MarketingPreference(models.Model):
  user = models.OneToOneField(User)
  subscribed = models.BooleanField(default=True)
  mailchimp_subscribed = models.NullBooleanField(blank=True)
  mailchimp_msg = models.TextField(null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.email