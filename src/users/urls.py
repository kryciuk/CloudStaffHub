from django.urls import path

from users.views import (DashboardView, LoginView, LogoutView,
                         ProfileDetailView, RegisterView,
                         UserProfileUpdateView)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profiles/<int:pk>", ProfileDetailView.as_view(), name='profile'),
    path("profiles/<int:pk>/edit", UserProfileUpdateView.as_view(), name='profile-edit')
]
