
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("post", views.post, name="post"),
    path("register", views.register, name="register"),

    #API Routes
    path("followers/<int:user_id>", views.followers, name="followers"),

    path("<str:username>", views.profile, name="profile")
]