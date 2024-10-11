from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View
from django.views.generic import ListView

from django.urls import reverse_lazy
#--------------------------


from .models import Category, Movie, Reviews, Genre
from .forms import ReviewForm
from .services import MovieService



class GenerateYear:
    """Жанры и год выхода фильма"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.all()


class FilterFilms(GenerateYear, ListView):
    """Фильтр фильма по жанрам т годам"""

    template_name = 'website/index.html'
    queryset = Movie.objects.all()

    def get_queryset(self):
        print(self.request.GET.getlist("genre"))
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genre__slug__in=self.request.GET.getlist("genre"))
        )
        return queryset


def index(request):
    return MovieService().get_home_page(request)


def detail_movies(request, slug):
    return MovieService().get_detail_page(request, slug)


def category_movies(request, slug):
    category = get_object_or_404(Category, slug=slug)
    movies = Movie.objects.filter(category=category)

    context = {
        'movies': movies
    }

    return render(request, 'website/index.html', context)


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            parent_id = request.POST.get("parent", None)
            if parent_id:
                form.parent_id = int(parent_id)

            form.movie = movie
            if request.user.is_authenticated:
                form.user = request.user
            form.save()
        return redirect("detail", slug=movie.slug)


class Search(ListView):
    """Реализация функционала поиска по названию"""
    # paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get('q')
        return context


"""
objects.get() - используется для фильрации по уникальному значению, может отдать только одно значение
objects.filter() - используется для фильтрации по любому значению, отдает список элементов либо пустой список
select * from table_name; Model.objects.all()
select * from table_name where поле_с_уникальным_значением=значение; Model.objects.get()
select * from table_name where поле_с_не_уникальным_значением=значение; Model.objects.filter()

"""


# filter класс python
# Model.objects.filter() - метод объекта objects