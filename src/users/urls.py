from django.urls import path

from users.views import (DashboardView, UserLoginView, UserLogoutView,
                         ProfileDetailView, RegisterView,
                         UserProfileUpdateView, UserPasswordResetView, UserPasswordResetDoneView,
                         UserPasswordResetConfirmView, UserPasswordResetCompleteView)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profiles/<int:pk>", ProfileDetailView.as_view(), name="profile"),
    path(
        "profiles/<int:pk>/edit", UserProfileUpdateView.as_view(), name="profile-edit"
    ),
]


urlpatterns_password = [
    path("password-reset", UserPasswordResetView.as_view(), name="password_reset"),
    path("password-reset-done", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete", UserPasswordResetCompleteView.as_view(), name="password_reset_complete")
]

urlpatterns += urlpatterns_password
