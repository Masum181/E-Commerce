from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from products.models import User as model_user

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class meta:
        model= User
        fields = ['username', 'email', 'password1', 'password2']
    
    

class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['image', 'location', 'phone_number', 'date_of_birth']
        
