"""
URL configuration for trendsfactory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("products/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("home/",views.HomeView.as_view(),name="home"),
    path("products/<int:pk>/add_to_basket/",views.AddToBasketView.as_view(),name="add-to-basket"),
    path("basket/items/all/",views.BasketItemListView.as_view(),name="basket-items"),
    path("basket/items/<int:pk>/remove/",views.BasketItemRemoveView.as_view(),name="basket-item-remove"),
    path("basket/items/<int:pk>/qty/change/",views.CartItemUpdateQuantityView.as_view(),name="edit-cart-qty"),
    path("checkout/",views.CheckOutView.as_view(),name="checkout"),
    path("signout/",views.SignOutView.as_view(),name="signout"),
    path("ordersummary/",views.OrderSummaryView.as_view(),name="order-summary"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
