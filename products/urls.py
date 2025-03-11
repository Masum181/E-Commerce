from django.urls import path
from .views import (
    ProductListView,
    ProductDetail,
    add_to_cart,
    cart,
    remove_cart,
    order_now, 
    order_history,
    FileFieldFormView
)


urlpatterns=[
    path('', ProductListView.as_view(), name='product-home'),
    path('<slug:slug>', ProductDetail.as_view(), name='product-detial'),
    path('add-to-cart/<id>/', add_to_cart, name='add_to_cart'),
    path('cart-items/', cart, name='cart-items'),
    path('remove-cart/<id>/', remove_cart, name='remove-cart'),
    path('order-now/', order_now, name='order'),
    path('order_history/', order_history, name='order_history'),
    path('multiple_upload/', FileFieldFormView.as_view(), name='multifile'),
    
]