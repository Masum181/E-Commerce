from django.contrib import admin
from .models import (Product,
                    Order, 
                    Cart, 
                    CartItem)
# from .forms import ProductCSVUploadForm

from django.utils.html import format_html



# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'location', 'gender', 'dob', 'country_of_birth')
#     search_fields = ('name', 'category', 'location')

# import csv
# import os
# from django.contrib import admin
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.conf import settings
# from .models import Product
# from .forms import ProductCSVUploadForm

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'image_preview')  # ✅ Show images in admin
#     actions = ['import_csv']  # ✅ Add import action

#     def image_preview(self, obj):
#         if obj.image:
#             return f'<img src="{obj.image.url}" width="50" height="50" />'
#         return "No Image"
#     image_preview.allow_tags = True
#     image_preview.short_description = "Image"

#     def import_csv(self, request, queryset=None):
#         """ Custom admin action to upload products via CSV and images """
#         if request.method == "POST":
#             form = ProductCSVUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#                 csv_file = request.FILES["csv_file"]
#                 image_files = request.FILES.getlist("image_files")  # ✅ Get list of images
#                 image_map = {image.name: image for image in image_files}  # ✅ Create image dictionary

#                 decoded_file = csv_file.read().decode("utf-8").splitlines()
#                 reader = csv.reader(decoded_file)
#                 next(reader)  # Skip the header row

#                 new_products = []
#                 for row in reader:
#                     if len(row) < 3:  # Ensure there are enough columns
#                         messages.error(request, "Invalid CSV format. Must include 'name', 'price', 'image'.")
#                         return render(request, "admin/csv_upload.html", {"form": form})

#                     name, price, image_filename = row[:3]
#                     image_file = image_map.get(image_filename.strip(), None)  # ✅ Match image file

#                     product = Product(name=name, price=price)
#                     if image_file:
#                         product.image.save(image_filename, image_file)  # ✅ Save image to Product
#                     new_products.append(product)

#                 Product.objects.bulk_create(new_products)  # ✅ Bulk insert into DB
#                 messages.success(request, f"Successfully imported {len(new_products)} products with images!")
#                 return redirect("..")

#         else:
#             form = ProductCSVUploadForm()

#         return render(request, "admin/csv_upload.html", {"form": form})

#     import_csv.short_description = "Import Products from CSV"

# admin.site.register(Product, ProductAdmin)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'brand', 'price', 'display_image')
    search_fields = ('name', 'category', 'brand')
    readonly_fields = ('display_image',) # prevent users from modifying images

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src={} width="50" height="50"/>', obj.image.url)
        return "No Image"
    display_image.short_description= 'Product Image'

    # Restrict Product management to superusers only
    def has_add_permission(self, request):
        return request.user.is_superuser # only superusers (developers) can add 

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser # only superuser can edit
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser # only super user can delete
    

def get_queryset(self, request):
    """
    If normal users can access Django admin (/admin/), they shouldn't see the Products section."""
    if not request.user.is_superuser:
        return self.model.objects.none()  # Hide products for normal users
    return super().get_queryset(request)

    


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'timestamp', 'location')
    search_fields = ('user__name', 'product__name')

# admin.site.register(Cart)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid')
    search_fields = ('user__username',)

# admin.site.register(CartItem)
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product')
    search_fields = ('product__title',)
# admin.site.register(History)

