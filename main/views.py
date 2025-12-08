from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import RegisterForm, PostForm
from .models import Profile, Post
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        
    else:
        form = RegisterForm()
    return render(request, "main/register.html", {"form": form})

class LoginView(auth_views.LoginView):
    template_name = "main/login.html"

class LogoutView(auth_views.LogoutView):
    pass

@login_required
def home_view(request):
    view_mode = request.GET.get("view", "following")
    post_form = PostForm()

    if request.method == "POST" and "create_post" in request.POST:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")

    if view_mode == "all":
        posts = Post.objects.all()

    else:
        following_profiles = request.user.profile.following.all()
        following_users = [p.user for p in following_profiles]
        posts = Post.objects.filter(author__in=following_users) | Post.objects.filter(author=request.user)
        posts = posts.order_by("-created_at")

    return render(request, "main/home.html", {
        "view_mode": view_mode,
        "posts": posts,
        "post_form": post_form
    })

@login_required
def profile_view(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = target_user.profile
    is_following = request.user.profile.following.filter(pk=profile.pk).exists()

    if request.method == "POST" and "toggle_follow" in request.POST:
        if is_following:
            request.user.profile.following.remove(profile)
        else:
            request.user.profile.following.add(profile)
        return redirect("profile", username=username)
    
    return render(request, "main/profile.html", {
        "target_user": target_user,
        "profile": profile,
        "is_following": is_following,
    })