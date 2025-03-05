from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    
    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs.get("slug"))
    

class ProductDetail(DetailView):
    model = Product
    template_name = 'products/item.html'
    context_object_name = 'products'
    
