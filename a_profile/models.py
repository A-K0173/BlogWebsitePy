from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Follow

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_followers_count(self):
        return Follow.objects.filter(followed=self.user).count()
    
    def get_following_count(self):
        return Follow.objects.filter(follower=self.user).count()
    
    def is_following_user(self, target_user):
        return Follow.objects.filter(
            follower=self.user,
            followed=target_user
        ).exists()
    
    def get_suggested_users(self, limit=10):
        """Get users to suggest for following (not already following)"""
        following_ids = Follow.objects.filter(
            follower=self.user
        ).values_list('followed_id', flat=True)
        
        # Exclude self and already followed users
        suggested_users = User.objects.exclude(
            id__in=list(following_ids) + [self.user.id]
        ).order_by('-date_joined')[:limit]
        
        return suggested_users