from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:user_id>/', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
]
