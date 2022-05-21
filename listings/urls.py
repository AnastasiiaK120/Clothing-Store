from django.urls import path

from .views import front, product_list, product_detail, submit_review

app_name = 'listings'

urlpatterns = [
    path('', front,  name='front'),
    path('shop/', product_list, name='shop'),
    path('shop/<slug:slug>/', product_detail, name='product'),
path('shop/<slug:slug>/submit_review/', submit_review, name='submit_review'),

]