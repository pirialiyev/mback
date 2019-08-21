from django.shortcuts import render
from billing.models import *
from billing.api import *
from .forms import *
from magazine.api import *
from backend.api import UserSerializer, UserManager, ProductSerializer
from django.views.generic import TemplateView
from magazine.models import *
from products.models import *
from backend.models import *
from addresses.api import *
from addresses.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.http import Http404, HttpResponse
from backend.utils import render_to_pdf
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from orders.models import ProductPurchase

class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    #renderer_classes = (JSONRenderer, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AboutView(TemplateView):
  template_name = "about.html"

  def get_context_data(self, **kwargs):
    context = super(AboutView, self).get_context_data(**kwargs)
    context['title'] = 'About page'
    context['content'] = ""
    return context

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    #lookup_field = 'slug'
    #lookup_value_regex = '[0-9a-f]{32}'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class CardViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class ChargeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer


class BillingProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    queryset = BillingProfile.objects.all()
    serializer_class = BillingProfileSerializer



class MagazineViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer


class ProductListView(ListView):
    model = AddProducts 
    context_object_name = 'dashboard'
    def get_queryset(self):
        
        return Product.objects.all()

class ProductCreateView(LoginRequiredMixin ,CreateView):
    model = Product
    form_class = AddProducts
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('dashboard_add')

    def get_queryset(self):
        return Product.objects.all()

class ProductUpdateView(UpdateView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)
                      
    model = Product
    form_class = AddProducts
    template_name = 'dashboard/product_update_form.html'
    success_url = reverse_lazy('dashboard_add')