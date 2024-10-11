from django.db.models import Q
from django import template
from website.models import Category, Genre, Movie


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_genre():
    return Genre.objects.all()


@register.simple_tag()
def get_movies_years():
    movies = Movie.objects.all().values_list('year').order_by('year')
    movies = sorted(set(movies))
    return list(map(lambda x: x[0], movies))


# @register.simple_tag(takes_context=True)
# def filter_movies(context):
#     request = context['request']
#     selected_genres = request.GET.getlist('genre')  # Получаем список выбранных жанров
#     selected_years = request.GET.getlist('year')  # Получаем список выбранных годов
#
#     queryset = Movie.objects.all()  # Начинаем с полного набора объектов Movie
#
#     if selected_genres or selected_years:
#         # Создаем условие фильтрации с использованием Q объектов
#         query = Q()
#         if selected_genres:
#             query &= Q(genre__id__in=selected_genres)
#         if selected_years:
#             query &= Q(year__in=selected_years)
#         queryset = queryset.filter(query)

    # return queryset.distinct()  # Возвращаем уникальные объекты Movie


@register.simple_tag()
def last_movies(count=10):
    return Movie.objects.order_by('-created_at')[:count]


