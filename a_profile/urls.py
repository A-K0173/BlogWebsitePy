from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:user_id>/', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'),
    path('user/<int:user_id>/followers/', views.followers_list, name='followers_list'),
    path('user/<int:user_id>/following/', views.following_list, name='following_list'),
]