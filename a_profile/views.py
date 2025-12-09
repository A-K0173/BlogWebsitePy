from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from blog.models import Post, Like, Comment, Follow

def profile_view(request, user_id):
    """View a user's profile with their posts, liked posts, and commented posts"""
    profile_user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=profile_user)
    
    # Get follow stats
    followers_count = Follow.objects.filter(followed=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    
    # Get lists of followers and following (limited to show in collapse)
    followers = Follow.objects.filter(followed=profile_user).select_related('follower')[:10]
    following = Follow.objects.filter(follower=profile_user).select_related('followed')[:10]
    
    # Check if current user is following this profile user
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user, 
            followed=profile_user
        ).exists()
    
    # Get user's posts
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    # Get posts the user liked
    liked_posts = Post.objects.filter(like__user=profile_user).distinct().order_by('-created_at')[:5]
    
    # Get posts the user commented on
    commented_posts = Post.objects.filter(comment__user=profile_user).distinct().order_by('-created_at')[:5]
    
    # Check if the user is viewing their own profile
    is_own_profile = request.user == profile_user
    
    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'liked_posts': liked_posts,
        'commented_posts': commented_posts,
        'is_own_profile': is_own_profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers': followers,
        'following': following,
        'is_following': is_following,
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

@login_required
def follow_toggle(request, user_id):
    """Follow or unfollow a user"""
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Don't allow following yourself
    if request.user == user_to_follow:
        return redirect('profile', user_id=user_id)
    
    # Check if already following
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=user_to_follow
    )
    
    if not created:
        # Unfollow if already following
        follow.delete()
    
    return redirect('profile', user_id=user_id)

@login_required
def followers_list(request, user_id):
    """View all followers of a user"""
    user = get_object_or_404(User, id=user_id)
    followers = Follow.objects.filter(followed=user).select_related('follower')
    
    return render(request, 'a_profile/followers_list.html', {
        'user': user,
        'followers': followers
    })
# god help me
@login_required
def following_list(request, user_id):
    """View all users that a user is following"""
    user = get_object_or_404(User, id=user_id)
    following = Follow.objects.filter(follower=user).select_related('followed')
    
    return render(request, 'a_profile/following_list.html', {
        'user': user,
        'following': following
    })