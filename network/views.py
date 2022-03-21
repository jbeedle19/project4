import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj
    })


@login_required(login_url="/login", redirect_field_name=None)
def following(request):
    currentUser = User.objects.get(id=request.user.id)
    following = currentUser.followers.all()
    posts = []

    for person in following:
        allPosts = person.posts.all()
        for post in allPosts:
            posts.append(post)

    posts.sort(key=lambda x: x.created, reverse=True)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        'page_obj': page_obj
    })


@login_required(login_url="/login", redirect_field_name=None)
def follow(request, user_id):
    profileOwner = User.objects.get(id=user_id)
    currentUser = User.objects.get(id=request.user.id)
    followers = profileOwner.following.all()

    if user_id != currentUser.id:
        if currentUser in followers:
            profileOwner.following.remove(currentUser.id)
        else:
            profileOwner.following.add(currentUser.id)

    return HttpResponseRedirect(reverse(profile, args=[profileOwner.username]))


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
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except User.DoesNotExist:
        profileOwner = None
        page_obj = None

    if user.username == username:
        currentUser = True
    else:
        currentUser = False

    return render(request, "network/profile.html", {
        'profileOwner': profileOwner,
        'page_obj': page_obj,
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


@login_required(login_url="/login", redirect_field_name=None)
def update(request, user_id, post_id, page):

    # Make sure person editing is the currentUser and that their id matches the posters id
    if user_id != request.user.id:
        return render(request, "network/error.html", {
            'message': 'You can only edit your own posts and not other users posts'
        })

    content = request.POST['content']

    # Check that post is not too long
    if len(content) > 300:
        return render(request, "network/error.html", {
            'message': 'Post is too long, must be 300 characters or less. Please edit your post and try again.'
        })

    # Update post
    post = Post.objects.get(id=post_id)
    post.content = content
    post.save()

    # Reload the page depending on which page they edited from
    if page == "profile":
        profileOwner = User.objects.get(id=user_id)
        return HttpResponseRedirect(reverse(profile, args=[profileOwner.username]))
    else:
        return HttpResponseRedirect(reverse("index"))


#API Routes
@csrf_exempt
@login_required(login_url="/login", redirect_field_name=None)
def like(request, post_id):
    user = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=post_id)

    like = Like(user=user, post=post)
    like.liked=True

    post.likes += 1
    post.user_likes.add(user)

    post.save()
    like.save()

    # No need to render because JS is handling that
    return HttpResponse(status=204)


@csrf_exempt
@login_required(login_url="/login", redirect_field_name=None)
def dislike(request, post_id):
    user = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=post_id)

    like = Like(user=user, post=post)
    like.liked=False

    post.likes -= 1
    post.user_likes.remove(user)

    post.save()
    like.save()

    # No need to render because JS is handling that
    return HttpResponse(status=204)