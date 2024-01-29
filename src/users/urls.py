from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (
    ProfileDetailView,
    ProfileUpdateView,
    RegisterView,
    UserInfoEditByOwnerView,
    UserLoginView,
    UserPasswordResetCompleteView,
    UserPasswordResetConfirmView,
    UserPasswordResetDoneView,
    UserPasswordResetView,
)

urlpatterns_authorization = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(template_name="users/authorization/logout.html"), name="logout"),
]

urlpatterns_profiles = [
    path("profiles/<int:pk>/update", ProfileUpdateView.as_view(), name="profile-update"),
    path("profiles/<int:pk>/edit", UserInfoEditByOwnerView.as_view(), name="profile-edit"),
    path("profiles/<int:pk>", ProfileDetailView.as_view(), name="profile"),
]

urlpatterns_password = [
    path("password-reset", UserPasswordResetView.as_view(), name="password_reset"),
    path("password-reset-done", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password-reset-complete", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

urlpatterns = urlpatterns_password + urlpatterns_profiles + urlpatterns_authorization
