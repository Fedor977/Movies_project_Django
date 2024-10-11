from django.shortcuts import render
from allauth.account.views import SignupView, LoginView, LogoutView
from django.urls import reverse_lazy


class CustomSignView(SignupView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login') # перенаправления на страницу авторизации после успешной регистрации


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('index') # перенаправления на главную страницу


class CustomLogout(LogoutView):
    template_name = 'users/logged_out.html'
    next_page = reverse_lazy('index') # перенаправления на главную страницу после выхода