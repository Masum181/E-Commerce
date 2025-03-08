from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import Order, Product, CartItem, Cart


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
