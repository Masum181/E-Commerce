from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .forms import OrderForm, FileFieldForm
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

import os
import csv

from django.conf import settings
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.edit import FormView


from .models import ( 
    Product, 
    Cart, 
    CartItem, 
    Order)

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
    

def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item = CartItem.objects.create(cart=cart, product=product)
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    price = 0
    for item in cart_items:
        price += item.product.price

    context = {'cart_items': cart_items, 'total_price': price}
    return render(request, 'products/cart.html', context=context)


@login_required
def order_now(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            cart_items = form.cleaned_data.get('cart_products', [])
            location = form.cleaned_data.get('location',[])
            delivary_time= form.cleaned_data.get('delivary_time', [])
            timestamp = now()

            if not cart_items:
                messages.error(request, "You Must Select at least one product")
                return redirect('order')
            orders = [
                Order(user=request.user, product=item.product, timestamp=timestamp, location=location, delivary_time=delivary_time)
                for item in cart_items
            ]
            Order.objects.bulk_create(orders)

            #Remove the ordered items from the cart
            cart_items.delete()

            messages.success(request, f"Your Order has been placed successfully")
            return redirect('product-home')

    else:
        form = OrderForm(user=request.user)
    return render(request, 'products/order.html', context= {'form': form})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'products/order_history.html', {'orders': orders})

class FileFieldFormView(UserPassesTestMixin, LoginRequiredMixin,FormView):
    form_class = FileFieldForm
    template_name = 'products/upload.html'
    success_url = '/'
    login_url = '/login/'

    def test_func(self):
        """Only allow superusers to access this view"""
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        """Redirect unauthorized users or show a 403 Forbidden error"""
        if not self.request.user.is_authenticated:
            return super().handle_no_permission() # Redirect to login page
        return HttpResponseForbidden('You are not allowed to upload files')
    

    def form_valid(self, form):
        files = form.cleaned_data['file_field']
        csv_file = form.cleaned_data['csv_file']
        print(type(csv_file))
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        for f in files:
            file_path = os.path.join(upload_dir, f.name)
            with open(file_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        
        decoded_csv_file = csv_file.read().decode('unicode_escape').splitlines()
        reader = csv.reader(decoded_csv_file)
        next(reader)
        new_products = []
        for row in reader:
            title, description,category, brand, price, image  = row[:6]
            slug = slugify(title)
            product = Product(title=title, description=description, category=category, brand=brand, price=price, image=image, slug=slug)
            # product.save()
            new_products.append(product)
        print("slugigfy come ")
        Product.objects.bulk_create(new_products) # Bulk insert into DB
        messages.success(self.request, f"Successfully import {len(new_products)} products with images!")
        return super().form_valid(form)

