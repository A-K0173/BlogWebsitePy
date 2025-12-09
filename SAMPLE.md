# Open Django shell: python manage.py shell
# Then paste and execute this entire script:

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
import django
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Like, Comment, Follow
from a_profile.models import UserProfile
from django.utils import timezone
import random

def create_sample_data():
    # Clear existing sample data (optional)
    print("Clearing existing sample data...")
    User.objects.filter(username__startswith='user_').delete()
    print("Existing sample users deleted.")
    
    # Create 5 users
    users = []
    for i in range(1, 6):
        username = f'user_{i}'
        email = f'user{i}@example.com'
        password = 'password123'
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        users.append(user)
        print(f"Created user: {username}")
    
    # Create user profiles (should be auto-created via signal, but let's ensure)
    for user in users:
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            profile.description = f"This is the profile description for {user.username}. Welcome to my blog!"
            profile.save()
            print(f"Created profile for: {user.username}")
    
    print("\n" + "="*50 + "\n")
    
    # Create sample posts (2-3 per user)
    posts = []
    for user in users:
        num_posts = random.randint(2, 3)
        for i in range(num_posts):
            post = Post.objects.create(
                title=f'{user.username}\'s Post {i+1}',
                content=f'This is the content of {user.username}\'s post number {i+1}. ' +
                        'This is a sample blog post about various topics. ' +
                        'Feel free to comment and like if you find this interesting!',
                author=user,
                created_at=timezone.now()
            )
            posts.append(post)
            print(f"Created post: '{post.title}' by {user.username}")
    
    print("\n" + "="*50 + "\n")
    
    # Create likes (each user likes 3-5 random posts)
    for user in users:
        num_likes = random.randint(3, 5)
        posts_to_like = random.sample(posts, min(num_likes, len(posts)))
        
        for post in posts_to_like:
            # Ensure user doesn't like their own post (optional)
            if post.author != user:
                like, created = Like.objects.get_or_create(
                    user=user,
                    post=post
                )
                if created:
                    print(f"{user.username} liked '{post.title}'")
    
    print("\n" + "="*50 + "\n")
    
    # Create comments (each user comments on 2-3 random posts)
    sample_comments = [
        "Great post! Thanks for sharing.",
        "I have a different perspective on this topic.",
        "This was really helpful, thank you!",
        "Can you elaborate more on this point?",
        "I completely agree with your views.",
        "Interesting take on the subject.",
        "Have you considered this alternative approach?",
        "Well written and informative.",
        "Looking forward to more posts like this!",
        "Thanks for the insights."
    ]
    
    for user in users:
        num_comments = random.randint(2, 3)
        posts_to_comment = random.sample(posts, min(num_comments, len(posts)))
        
        for post in posts_to_comment:
            # Ensure user doesn't comment on their own post (optional)
            if post.author != user:
                comment_text = random.choice(sample_comments)
                comment = Comment.objects.create(
                    user=user,
                    post=post,
                    content=f"{comment_text} - {user.username}"
                )
                print(f"{user.username} commented on '{post.title}': '{comment_text[:30]}...'")
    
    print("\n" + "="*50 + "\n")
    
    # Create follow relationships (each user follows 2-3 other users)
    for user in users:
        num_follows = random.randint(2, 3)
        # Get other users to follow
        other_users = [u for u in users if u != user]
        users_to_follow = random.sample(other_users, min(num_follows, len(other_users)))
        
        for followed_user in users_to_follow:
            follow, created = Follow.objects.get_or_create(
                follower=user,
                followed=followed_user
            )
            if created:
                print(f"{user.username} started following {followed_user.username}")
    
    print("\n" + "="*50 + "\n")
    
    # Create one admin user
    admin_user, created = User.objects.get_or_create(
        username='admin_user',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': False
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'description': 'This is the admin user profile.'}
        )
        print(f"Created admin user: admin_user (password: admin123)")
    
    # Display summary
    print("\n" + "="*50)
    print("SAMPLE DATA CREATION COMPLETE")
    print("="*50)
    print(f"Users created: {User.objects.filter(username__startswith='user_').count()}")
    print(f"Total posts: {Post.objects.count()}")
    print(f"Total likes: {Like.objects.count()}")
    print(f"Total comments: {Comment.objects.count()}")
    print(f"Total follows: {Follow.objects.count()}")
    print("\nLogin credentials for sample users:")
    print("-" * 30)
    for user in users:
        print(f"Username: {user.username}")
        print(f"Password: password123")
        print(f"Email: {user.email}")
        print("-" * 30)
    print("\nAdmin user:")
    print(f"Username: admin_user")
    print(f"Password: admin123")
    print("="*50)

if __name__ == '__main__':
    create_sample_data()

create_sample_data()