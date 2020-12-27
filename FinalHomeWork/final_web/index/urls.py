from django.urls import path

from . import views

urlpatterns = [
    path('<int:sku>', views.indexsku),
    path('search', views.search),
    path('', views.indexnull),
]
