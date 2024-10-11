from django.urls import path

from . import views

from allauth.account.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    PasswordChangeView,
    ConfirmEmailView
)


urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.FilterFilms.as_view(), name='filter_films'),
    path('search/', views.Search.as_view(), name='search'),
    path('category/<slug:slug>/', views.category_movies, name='category'),
    path('movie/<slug:slug>/', views.detail_movies, name='detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),

]


account = [
    path('password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('password/reset/key/<uidb36>/<key>/', PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('password/reset/key/done/', PasswordResetFromKeyDoneView.as_view(), name='account_reset_password_from_key_done'),
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('confirm-email/<key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
]


urlpatterns.extend(account) # добавляем маршруты account в список urlpatterns