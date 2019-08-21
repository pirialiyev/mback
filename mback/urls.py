from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from .views import *
from products.models import *
from django.views.generic import RedirectView
from products.views import HomePageListView
from django.conf import settings
from django.conf.urls.static import static
from carts.views import *
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'product', ProductViewSet)
router.register(r'address', AddressViewSet)
router.register(r'card', CardViewSet)
router.register(r'magazine', MagazineViewSet)
router.register(r'charge', ChargeViewSet)
router.register(r'billingprofil', BillingProfileViewSet)



#router.register(r'email-aktiv', EmailActivationViewSet)
#router.register(r'adress', AddressViewSet)
#router.register(r'object', ObjectViewedViewSet)
#router.register(r'session', UserSessionViewSet)





urlpatterns = [
  url(r'^login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
  url(r'^auth/', include('djoser.urls')),
  url(r'^auth/', include('djoser.urls.authtoken')),
  url(r'^auth/', include('djoser.urls.jwt')),
  url(r'^dashboard/', ProductListView.as_view(), name='dashboard'),
  url(r'^dashboard/add/', ProductCreateView.as_view(), name='dashboard_add'),
  #url(r'^dashboard/<int:pk>/edit/', ProductUpdateView.as_view(), name='dashboard_edit'),
  url(r'^rest/', include(router.urls)),
  url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
  urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

