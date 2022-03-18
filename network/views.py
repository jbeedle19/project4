import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like


def index(request):
    return render(request, "network/index.html", {
        'posts': Post.objects.all()
    })

@login_required(login_url="/login", redirect_field_name=None)
def following(request):
    return render(request, "network/following.html", {
        'posts': ['one', 'two', 'three']
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def post(request):
    content = request.POST['content']
    user = request.user

    if len(content) > 300:
        return render(request, "network/error.html", {
            'message': 'Post is too long, must be 300 characters or less. Please edit your post and try again.'
        })

    p = Post(user=user, content=content)
    p.save()

    return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    user = request.user
    try:
        profileOwner = User.objects.get(username=username)
        posts = profileOwner.posts.all()
    except User.DoesNotExist:
        profileOwner = None
        posts = None

    if user.username == username:
        currentUser = True
    else:
        currentUser = False

    return render(request, "network/profile.html", {
        'profileOwner': profileOwner,
        'posts': posts,
        'currentUser': currentUser
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

#API Routes
@csrf_exempt
@login_required
def followers(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)

    if request.method == 'GET':
        return JsonResponse(user.serialize())