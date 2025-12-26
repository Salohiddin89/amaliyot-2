from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("create/", views.post_create, name="post_create"),
    path("post-like/<int:pk>/", views.post_like, name="post_like"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("comment/add/<int:pk>/", views.add_comment, name="add_comment"),
    path("comment/delete/<int:pk>/", views.delete_comment, name="delete_comment"),
    path("post/delete/<int:pk>/", views.delete_post, name="delete_post"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("post/edit/<int:pk>/", views.edit_post, name="edit_post"),
    path("post/delete/<int:pk>/", views.delete_post, name="delete_post"),
]
