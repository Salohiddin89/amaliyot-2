from django.contrib import admin
from django.utils.html import format_html
from .models import User, Category, Post, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "get_avatar", "is_staff")
    search_fields = ("username", "email")

    def get_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%;" />',
                obj.avatar.url,
            )
        return "Rasm yo'q"

    get_avatar.short_description = "Avatar"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}  # Nom yozilsa slug avtomat to'ladi


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "view_count",
        "created_at",
        "get_image",
    )
    list_filter = ("category", "author", "created_at")  # O'ng tomonda filtr
    search_fields = ("title", "content")  # Qidiruv
    readonly_fields = ("view_count",)  # Ko'rishlar sonini qo'lda o'zgartirib bo'lmaydi
    date_hierarchy = "created_at"  # Vaqt bo'yicha navigatsiya

    def get_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 40px; border-radius: 5px;" />',
                obj.image.url,
            )
        return "Rasm yo'q"

    get_image.short_description = "Post rasmi"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
