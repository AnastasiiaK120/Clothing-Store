from django.urls import path

from .views import front, product_list

app_name = 'listings'

urlpatterns = [
    path('', front,  name='front'),
    path('shop/', product_list, name='shop'),
]