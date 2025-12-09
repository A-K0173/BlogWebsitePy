from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, Like, Comment, Follow
from .forms import PostForm, CommentForm

@login_required
def create_post(request):
    """
    Handles Blog post creation
    - GET: Show empty form for creating a new post
    - POST: Save the form and redirect to post detail
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def post_detail(request, pk):
    """View a single post with its comments and likes"""
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    liked = Like.objects.filter(post=post, user=request.user).exists()
    
    if request.method == 'POST':
        # Handle comment submission
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'liked': liked,
        'comment_form': comment_form
    })

@login_required
def post_list(request):
    """Show all posts or filtered posts"""
    posts = Post.objects.all().order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    # Filter by user if specified
    username = request.GET.get('user')
    if username:
        posts = posts.filter(author__username=username)
    
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def home_feed(request):
    """Show posts from users that the current user follows"""
    # Get users that current user follows
    following = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
    
    # Include current user's posts too
    following_users = list(following) + [request.user.id]
    
    # Get posts from followed users
    posts = Post.objects.filter(author__id__in=following_users).order_by('-created_at')
    
    return render(request, 'blog/feed.html', {'posts': posts})

@login_required
def update_post(request, pk):
    """Update an existing post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user owns the post
    if post.author != request.user:
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    """Delete a post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user owns the post
    if post.author != request.user:
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/confirm_delete.html', {'post': post})

@login_required
def like_post(request, pk):
    """Like or unlike a post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Check if already liked
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )
    
    if not created:
        # Unlike if already liked
        like.delete()
    
    return redirect('post_detail', pk=pk)

@login_required
def follow_user(request, user_id):
    """Follow or unfollow a user"""
    user_to_follow = get_object_or_404(User, pk=user_id)
    
    if request.user != user_to_follow:
        # Check if already following
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )
        
        if not created:
            # Unfollow if already following
            follow.delete()
    
    return redirect('post_list')

# Add a view for adding a comment to a post
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})