
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API routes
    path("posts", views.compose, name="compose"),
    path("posts/allposts/<int:pageNumber>", views.allPosts, name="allPosts"),
    path("user/<str:user>/<int:pageNumber>", views.user, name="user"),
    path("followers/<str:user>", views.followers, name="followers"),
    path("following/<int:pageNumber>", views.following, name="following"),
    path("edit/<int:postID>", views.edit, name="edit"),
    path("like/<int:postID>", views.like, name="like")
]
