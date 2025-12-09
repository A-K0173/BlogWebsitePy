from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm


def login_view(request):
    """
    Handles login:
    - GET: show login form
    - POST: authenticate and log in user
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")   # Always return a response
        else:
            messages.error(request, "Invalid username or password.")

    # Make sure to return for get request or failed login
    return render(request, "accounts/login.html")


def register_view(request):
    """
    Handles user registration.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create user but don't save password yet
            user = form.save(commit=False)

            # Set the password properly
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    """Logs user out."""
    logout(request)
    return redirect("login")



