from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Home page view
def home_view(request):
    return render(request, "home/home.html")