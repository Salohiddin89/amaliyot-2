from django.db import models
from django.contrib.auth.models import AbstractUser


# Maxsus User modeli
# models.py ni shunday qoldiring:
class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", default="default.png")

    def __str__(self):
        return self.username


# Profile modelini o'chirib tashlang, u ortiqcha.


# Kategoriya modeli
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# Post modeli
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts/")
    video = models.FileField(
        upload_to="videos/", blank=True, null=True
    )  # Fayl ko'rinishida video
    short_description = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="blog_likes", blank=True)


class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="views")
    ip = models.CharField(max_length=45)  # Foydalanuvchi IP manzili

    class Meta:
        unique_together = ("post", "ip")  # Bitta IP bitta post uchun faqat 1 marta


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"
