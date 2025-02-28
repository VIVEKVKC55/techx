from django.urls import path
from .views import register, user_login, user_logout,forgot_password_request,reset_password

app_name="user"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("forgot-password/", forgot_password_request, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", reset_password, name="reset_password"),
]

