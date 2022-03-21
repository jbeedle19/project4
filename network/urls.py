
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("post", views.post, name="post"),
    path("register", views.register, name="register"),

    #API Routes

    path("<str:username>", views.profile, name="profile")
]