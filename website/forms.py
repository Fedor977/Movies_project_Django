from django import forms

from .models import Reviews

from allauth.account.forms import SignupForm, LoginForm
from users.models import User


class ReviewForm(forms.ModelForm):
    """Формы отзыва"""
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')



class CustomSignupForm(SignupForm):
    # Используем форму SignupForm от django-allauth и переопределяем её для нашей модели
    class Meta:
        model = User  # Указываем модель, которую будем использовать
        fields = ('username', 'email', 'password1', 'password2')  # Определяем поля формы


class CustomLoginForm(LoginForm):
    # Используем форму LoginForm от django-allauth и переопределяем её для нашей модели
    class Meta:
        model = User  # Указываем модель, которую будем использовать
        fields = ('username', 'password')  # Определяем поля формы
