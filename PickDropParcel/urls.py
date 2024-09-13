"""
URL configuration for PickDropParcel project.

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
from PickDropApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home),
    path('user_registration',views.register_user,name='user_registration'),
    path('login/',views.login,name='login'),
    path('pro_registration',views.professional_registration,name='pro_registration'),
    path('demo/',views.demo_page),
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('pro_login/',views.professional_login),
    path('pro_dashboard/',views.professional_dashboard),
    path('order_reject/<int:id>/',views.order_reject,name='order_reject'),
    path('order_accept/<int:id>/',views.order_accept, name='order_accept'),
    path('order_nevigate/<int:id>',views.order_nevigate),
    path('api/get-coordinates/<int:id>',views.get_coordinates,name='get_coordinates'),
]

urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)