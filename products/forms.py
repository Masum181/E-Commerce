from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import Order, Product, CartItem, Cart
from django.core.validators import FileExtensionValidator

# class OrderForm(forms.Form):
#     location = forms.CharField(max_length=50, required=True, label='Delivary Location')
#     delivary_time = forms.DateTimeField(
#         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         required=True,
#         label="Delivary Time"
#     )

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None) # Get Logged in User
#         print('user: ', user)
#         cart = Cart.objects.get(is_paid=False, user=user)
#         super().__init__(*args, **kwargs)

#         if user:
#             cart_items = CartItem.objects.filter(cart=cart)
#             print('cart_items_form', cart_items)
#             self.fields['Cart_products'] = forms.ModelMultipleChoiceField(
#                 queryset=cart_items,
#                 widget=forms.CheckboxSelectMultiple,
#                 required=True,
#                 label='Select Products from Cart'
#             )


class OrderForm(forms.Form):
    location = forms.CharField(max_length=50, required=True, label="Delivery Location")
    delivary_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        label="Delivery Time"
    )
    cart_products = forms.ModelMultipleChoiceField(
        queryset=CartItem.objects.none(),  # Initially empty
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Products from Cart"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get logged-in user
        super().__init__(*args, **kwargs)  # ✅ Move this before accessing the database

        print("User:", user)  # Debugging output

        # Ensure the user is logged in
        if user is not None:
            try:
                cart = Cart.objects.get(is_paid=False, user=user)  # ✅ Handle cases where cart might not exist
                cart_items = CartItem.objects.filter(cart=cart)
                # print("Cart Items in Form:", cart_items)  # Debugging output

                # ✅ Fix field name (must match cleaned_data)
                self.fields['cart_products'].queryset = cart_items
                self.fields['cart_products'].label_from_instance = lambda obj: f"{obj.product.title})"
            except Cart.DoesNotExist:
                print("No unpaid cart found for user.")  # Debugging output







# class ProductCSVUploadForm(forms.Form):
#     csv_file = forms.FileField(label="Upload CSV File")
    
#     # ✅ FIX: Allow multiple files using FileField + clean method
#     image_files = forms.FileField(
#         label="Upload Images", 
#         required=False,
#         widget=forms.FileInput(attrs={"multiple": True})  # ✅ FIX: Use `FileInput`
#     )

#     def clean_image_files(self):
#         """ ✅ Validate multiple images and return them as a list """
#         images = self.files.getlist("image_files")  # ✅ Retrieve multiple files
#         if not images:
#             return []
#         return images  # ✅ Return the list of images



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)
    
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
    
class FileFieldForm(forms.Form):
    file_field =  MultipleFileField()
    csv_file = forms.FileField(label='Upload CSV File',
                               validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    