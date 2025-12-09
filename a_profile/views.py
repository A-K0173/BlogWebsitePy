from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from blog.models import Post, Like, Comment

def profile_view(request, user_id):
    """View a user's profile with their posts, liked posts, and commented posts"""
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    # Get user's posts
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    
    # Get posts the user liked
    liked_posts = Post.objects.filter(like__user=user).distinct().order_by('-created_at')
    
    # Get posts the user commented on
    commented_posts = Post.objects.filter(comment__user=user).distinct().order_by('-created_at')
    
    # Check if the user is viewing their own profile
    is_own_profile = request.user == user
    
    context = {
        'profile_user': user,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'liked_posts': liked_posts,
        'commented_posts': commented_posts,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'a_profile/profile.html', context)

@login_required
def edit_profile(request):
    """Edit the current user's profile"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'a_profile/edit_profile.html', {'form': form})
