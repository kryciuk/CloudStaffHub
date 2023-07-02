# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.views.generic import View
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import CreateUserForm
#
#
# class WelcomeView(View):
#     def get(self, request):
#         context = {'title': 'Welcome'}
#         return render(request, 'users/welcome.html', context)
#
#
# class DashboardView(LoginRequiredMixin, View):
#
#     def get(self, request):
#         context = {'title': 'Dashboard'}
#         return render(request, 'users/dashboard.html', context)
#
#
# class LoginView(View):
#
#     def post(self, request):
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.warning(request, 'Your login details are incorrect')
#         context = {'title': 'Login'}
#         return render(request, 'users/login.html', context)
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('dashboard')
#         context = {'title': 'Login'}
#         return render(request, 'users/login.html', context)
#
#
# class RegisterView(View):
#
#     def post(self, request):
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {user}')
#             return redirect('login')
#         context = {'form': form, 'title': 'Register'}
#         return render(request, 'users/register.html', context)
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('dashboard')
#         form = CreateUserForm()
#         context = {'form': form, 'title': 'Register'}
#         return render(request, 'users/register.html', context)
#
#
# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         context = {'title': 'Logout'}
#         return render(request, 'users/logout.html', context)
