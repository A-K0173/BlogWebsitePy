from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Home page view
@login_required
def home_view(request):
    """Homepage shown only to logged-in users."""
    return render(request, "home/home.html")