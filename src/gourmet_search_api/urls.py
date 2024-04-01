from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop_details/', views.shop_details, name='shop_details'),
    path('fetch_shops/', views.fetch_shops, name='fetch_shops'),
    path('fetch_shop_details/', views.fetch_shop_details, name='fetch_shop_details'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('favorites/', views.favorites, name='favorites'),
]
