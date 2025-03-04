from django.urls import path
from .views import register, user_login, user_logout,forgot_password_request,reset_password
from .cus_view.dashboard import ProfileView, UserProductListView, CustomPasswordChangeView, UserViewedProductsView, UsersWhoViewedMyProductsView, SubscriptionUpgradeView


app_name="user"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("forgot-password/", forgot_password_request, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", reset_password, name="reset_password"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("user-products/", UserProductListView.as_view(), name="user-products"),
    path("change-password/", CustomPasswordChangeView.as_view(), name="change-password"),
    path("my-viewed-products/", UserViewedProductsView.as_view(), name="my-viewed-products"),
    path("users-who-viewed-my-products/", UsersWhoViewedMyProductsView.as_view(), name="users-who-viewed-my-products"),
    path("plan-upgrade/", SubscriptionUpgradeView.as_view(), name="subscription_upgrade"),
]
