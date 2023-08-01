from django.urls import path

from users.views import (AdminCompanyView, DashboardView, LoginView,
                         LogoutView, ProfileDetailView, RegisterCompanyView,
                         RegisterView, UserProfileUpdateView, WelcomeView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", WelcomeView.as_view(), name="welcome"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("register-company/", RegisterCompanyView.as_view(), name="register-company"),
    path("admin-company/", AdminCompanyView.as_view(), name="admin-company"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name='profile'),
    path("profile/<int:pk>/edit", UserProfileUpdateView.as_view(), name='profile-edit')
]
