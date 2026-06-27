from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, auth as django_auth


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("firstname", "").strip()
        last_name = request.POST.get("lastname", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        if not all([first_name, last_name, username, email, password, password2]):
            messages.error(request, "All fields are required.")
            return redirect("register")
        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is taken")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "That email is being used")
            return redirect("register")
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        django_auth.login(request, user)
        messages.success(request, "You are now logged in")
        return redirect("index")
    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("login")
        user = django_auth.authenticate(username=username, password=password)
        if user is not None:
            django_auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("dashboard")
        messages.error(request, "Invalid credentials")
        return redirect("login")
    return render(request, "accounts/login.html")


def logout_view(request):
    if request.method == "POST":
        django_auth.logout(request)
        messages.success(request, "Logout")
        return redirect("index")
    return redirect("index")
