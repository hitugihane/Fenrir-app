from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop_details/', views.shop_details, name='shop_details'),
    path('fetch_shops/', views.fetch_shops, name='fetch_shops'),
    path('fetch_shop_details/', views.fetch_shop_details, name='fetch_shop_details'),
]
