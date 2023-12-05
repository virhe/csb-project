from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def home(request):
    username = request.session.get("username", "default")
    return render(request, "home.html", {"username": username})


def login(request):
    login_message = ""
    if request.method == "POST":
        request.session["username"] = "default"
        username = request.POST.get("username")
        password = request.POST.get("password")

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM auth_user WHERE username = '{username}' AND password = '{password}'")
        success = cursor.fetchall()
        cursor.close()

        # success = authenticate(request, username=username, password=password)

        if not success:
            return render(request, "login.html")

        # login(request, success)

        request.session["_auth_user_id"] = success[0]
        request.session["username"] = username

        return redirect("home")

    else:
        request.session["username"] = "default"
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect("login")
        # else:
        #     form = UserCreationForm()

        request.session["username"] = "default"
        username = request.POST.get("username")
        password = request.POST.get("password")

        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO auth_user (password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) VALUES ('{password}', '', False, '{username}', '', '', False, True, '', '')")
        success = cursor.fetchone()
        cursor.close()

        return render(request, "login.html")

    else:
        request.session["username"] = "default"
        return render(request, "register.html")


def logout(request):
    request.session.flush()
    return redirect("home")

