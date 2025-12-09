from django.urls import path
from . import views

urlpatterns = [
	path('create/', views.create_post, name='create_post'),
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('feed/', views.home_feed, name='home_feed'),
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
]