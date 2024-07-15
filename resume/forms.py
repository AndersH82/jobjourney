from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'text-center'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'text-center'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'text-center'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'text-center'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'country', 'phone']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address', 'class': 'text-center'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter your country', 'class': 'text-center'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'text-center'}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=255)
    country = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                country=self.cleaned_data['country'],
                phone=self.cleaned_data['phone'],
                image=self.cleaned_data['image'] if 'image' in self.cleaned_data else 'default.jpg'
            )
        return user