"""csd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from main import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', views.sign_up),
    path('sign_in/', views.sign_in),
    path('vendor/', views.vendor_profile,name='vendor'),
    path('product/<str:pk>', views.product,name='product'),
    path('delete/<str:pk>', views.delete_task,name='delete'),
    path('store/', views.store,name='store'),
    path('cart/<str:pk>', views.cart,name='cart'),
    path('quantity/<str:pk>', views.quantity,name='quantity'),
    path('carts/', views.carts,name='carts'),
    path('money/', views.money,name='money'),
    path('order/', views.order,name='order'),
    path('previous/', views.previous,name='previous'),
    path('prev/', views.previous_vendor,name='previous_vendor'),
    path('del/<str:pk>', views.delet,name='del'),
    path('accounts/', include('allauth.urls')),
    path('choice/', views.choice,name='choice'),
    path('signout/',views.sign_out,name='signout'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)