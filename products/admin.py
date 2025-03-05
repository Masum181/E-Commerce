from django.contrib import admin
from .models import User, Product, Order
from django.utils.html import format_html


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'location', 'gender', 'dob', 'country_of_birth')
    search_fields = ('name', 'category', 'location')

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
    list_display = ('id', 'user', 'product', 'timestamp')
    search_fields = ('user__name', 'product__name')

