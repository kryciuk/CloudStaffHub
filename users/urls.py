from django.urls import path
from users.views import LoginView, RegisterView, LogoutView, WelcomeView, DashboardView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', WelcomeView.as_view(), name='welcome'),
    path('dashboard/', DashboardView.as_view(), name='dashboard')
]