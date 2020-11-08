from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.index),
    path('douban/', views.index),
    path('douban/search/', views.search)
]