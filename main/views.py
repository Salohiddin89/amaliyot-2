from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment, PostView, User
from .form import RegisterForm, PostForm, UserUpdateForm, PostUpdateForm


# --- ASOSIY SAHIFA ---
def index(request):
    categories = Category.objects.all()
    cat_slug = request.GET.get("cat")

    if cat_slug:
        posts = Post.objects.filter(category__slug=cat_slug).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")

    return render(request, "index.html", {"posts": posts, "categories": categories})


# --- POST DETAL VA O'XSHASH POSTLAR ---
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # IP orqali ko'rishlar sonini oshirish
    ip = get_client_ip(request)
    if not PostView.objects.filter(post=post, ip=ip).exists():
        PostView.objects.create(post=post, ip=ip)
        post.view_count += 1
        post.save()

    # O'xshash postlar (bir xil kategoriyadagi boshqa postlar)
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:3]
    # So'nggi postlar
    latest_posts = Post.objects.all().order_by("-created_at").exclude(id=post.id)[:5]

    return render(
        request,
        "post_detail.html",
        {"post": post, "related_posts": related_posts, "latest_posts": latest_posts},
    )


# --- USER PROFILI (BIOGRAFIA VA POSTLAR) ---
def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=target_user).order_by("-created_at")

    # Foydalanuvchi like bosgan hamma postlarni olish
    # Post modelida 'likes' RelatedName bo'lishi kerak
    liked_posts = Post.objects.filter(likes=target_user).order_by("-created_at")

    context = {
        "target_user": target_user,
        "posts": posts,
        "liked_posts": liked_posts,
    }
    return render(request, "profile.html", context)  # --- POST YARATISH ---


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # FILES rasm va video uchun shart
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "post_form.html", {"form": form})


# --- COMMENT QO'SHISH (REPLY BILAN) ---
@login_required
def add_comment(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        text = request.POST.get("text")
        parent_id = request.POST.get("parent_id")

        if text:
            parent_obj = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
            Comment.objects.create(
                post=post, user=request.user, text=text, parent=parent_obj
            )
    return redirect("post_detail", pk=pk)


# --- COMMENT O'CHIRISH (SIZDA URLBOR EDI) ---
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    post_id = comment.post.id
    comment.delete()
    return redirect("post_detail", pk=post_id)


# --- POST O'CHIRISH ---
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return redirect("user_profile", username=request.user.username)


# --- LIKE TIZIMI ---

def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Likeni olib tashlash
    else:
        post.likes.add(request.user)  # Like qo'shish

    # Eng muhim joyi: foydalanuvchi qayerdan bosgan bo'lsa, o'sha sahifaga qaytaradi
    return redirect(request.META.get("HTTP_REFERER", "post_detail"))


# --- AUTH (LOGIN, REGISTER, LOGOUT) ---
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


# --- YORDAMCHI FUNKSIYA ---
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


# Profilni tahrirlash
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_profile", username=request.user.username)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "edit_profile.html", {"form": form})


# Postni tahrirlash
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostUpdateForm(instance=post)
    return render(request, "edit_post.html", {"form": form, "post": post})
