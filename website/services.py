from . import models
from django.shortcuts import render


class MovieService:
    movies = models.Movie.objects.all()

    def get_home_page(self, request):
        return render(request, 'website/index.html', {
            'movies': self.movies
        })

    def get_detail_page(self, request, slug):
        movie = models.Movie.objects.get(slug=slug)
        reviews = movie.reviews.filter(parent=None)

        context = {
            'movie': movie,
            'reviews': reviews
        }
        return render(request, 'website/detail_movie.html', context)

