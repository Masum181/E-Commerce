from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from products.models import Cart, Product, CartItem

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile-pics')
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width> 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False, cart__user=self.user).count()

    
        