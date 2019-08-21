from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy

from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from .mixins import CsrfExemptMixin




class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
  form_class = MarketingPreferenceForm
  template_name = 'base/forms.html'
  success_url = reverse_lazy('marketing:email')
  success_message = 'Your email preferences have been updated. Thank you.'

  def dispatch(self, *args, **kwargs):
    user = self.request.user
    if not user.is_authenticated():
      return redirect(reverse('accounts:login') + '?next=' + reverse('marketing:email'))
    return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

  def get_context_data(self, *args, **kwargs):
    context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
    context['title'] = 'Update Email Preferences'
    context['next'] = 'Update Email Preferences'
    return context

  def get_object(self):
    user = self.request.user
    obj, created = MarketingPreference.objects.get_or_create(user=user)
    return obj


