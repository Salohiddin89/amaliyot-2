from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "avatar", "bio")


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Foydalanuvchi nomi"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Parol"})
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Bu yerda video_url bo'lsa o'chirib, video deb yozing
        fields = ["category", "title", "image", "video", "short_description", "content"]

    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "bio", "avatar"]


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "image",
            "video",
            "short_description",
            "content",
        ]  # Video qo'shildi
