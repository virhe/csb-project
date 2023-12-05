from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    username = request.session.get("username", "default")
    return render(request, "home.html", {"username": username})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM auth_user WHERE username = '{username}' AND password = '{password}'")
        success = cursor.fetchone()
        cursor.close()

        if not success:
            request.session["username"] = "default"
            return render(request, "login.html")

        user = User.objects.get(username=username)
        request.session["_auth_user_id"] = user.pk
        request.session["username"] = username

        return redirect("home")

    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO auth_user (password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) VALUES ('{password}', '', False, '{username}', '', '', False, True, '', '')")
        success = cursor.fetchone()
        cursor.close()

        return render(request, "login.html")

    else:
        return render(request, "register.html")


def logout(request):
    request.session.flush()
    return redirect("home")

