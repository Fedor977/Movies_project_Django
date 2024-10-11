from django.urls import path
from . import views


app_name = 'users'

"""
app_name - идентификатор ссылок приложения

reverse('signup') - НЕПРАВИЛЬНО
reverse('users:signup')

app: movies app_name = 'movies'
    movies:home
app: website app_name = 'website'
    website:home


{% url 'home' %}
{% url 'movies:home' %} - главная страница приложения movies
{% url 'website:home' %} - главная страница приложения website

"""

urlpatterns = [
    path('signup/', views.CustomSignView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogout.as_view(), name='logout')
]