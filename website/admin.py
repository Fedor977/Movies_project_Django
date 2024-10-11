from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ['id', 'title']


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ['id', 'title']


class MovieGalleryInline(admin.TabularInline):
    model = models.MovieGallery
    extra = 1
    max_num = 5


class ActorInline(admin.TabularInline):
    model = models.Actor


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'year', 'category']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['year', 'genre', 'category']
    inlines = [MovieGalleryInline, ActorInline]


@admin.register(models.Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['movie', 'text', 'user', 'parent']