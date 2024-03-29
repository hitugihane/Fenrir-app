from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch_shops/', views.fetch_shops, name='fetch_shops'),
]
