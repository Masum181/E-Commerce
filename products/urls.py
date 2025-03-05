from django.urls import path
from .views import (
    ProductListView,
    ProductDetail
)


urlpatterns=[
    path('', ProductListView.as_view(), name='product-home'),
    path('<slug:slug>', ProductDetail.as_view(), name='product-detial')
    
]