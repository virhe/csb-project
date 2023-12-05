"""
URL configuration for csb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vulnerable.views import home, login, register, logout, adminpanel
from django.db import connection

cursor = connection.cursor()
cursor.execute(f"SELECT * FROM auth_user WHERE username = 'admin' AND password = 'admin'")
success = cursor.fetchone()

if not success:
    # A02:2021 - Cryptographic Failures | CWE-259: Use of Hard-coded Password
    # A04:2021 - Insecure Design | CWE-312: Cleartext Storage of Sensitive Information
    cursor.execute(f"INSERT INTO auth_user (password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) VALUES ('admin', '', True, 'admin', '', '', True, True, '', '')")
cursor.close()

urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("adminpanel/", adminpanel, name="adminpanel")
]
