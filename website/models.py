from django.db import models
from django.template.defaultfilters import slugify
from users.models import User


class Genre(models.Model):
    title = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Movie(models.Model):
    title = models.CharField(max_length=225, verbose_name='Название фильма')
    slogan = models.CharField(max_length=260, verbose_name='Слоган')
    country = models.CharField(max_length=70, verbose_name='Страна')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    producer = models.CharField(max_length=100, verbose_name='Режиссер')
    genre = models.ManyToManyField('Genre', related_name='genre', null=True)
    premier_date = models.DateField(verbose_name='Дата выхода')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория фильма', related_name='category')
    slug = models.SlugField()
    budget = models.PositiveBigIntegerField(verbose_name='Бюджет фильма')
    fees_usa = models.PositiveBigIntegerField(verbose_name='Сборы в США')
    fees_world = models.PositiveBigIntegerField(verbose_name='Сборы в мире')
    poster = models.ImageField(upload_to='previews/', verbose_name='Постер')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    video = models.FileField(upload_to='media/videos/', verbose_name='Видео', blank=True, null=True)
    rating = models.FloatField(verbose_name='Рейтинг фильма', default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Был добавлен', null=True)

    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews_set.filter(parrent__isnull=True)  # метод get_review отдает список отзыв прикрепленных к фильму, фильтруя где parrent это null

    class Meta:
        verbose_name = 'фильм'
        verbose_name_plural = 'фильмы'


class Actor(models.Model):
    fullname = models.CharField(max_length=225, verbose_name='актер')
    movie_id = models.ForeignKey(verbose_name='актеры', on_delete=models.CASCADE, to=Movie, related_name='actors')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'актер'
        verbose_name_plural = 'актеры'


class Category(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название категории')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class MovieGallery(models.Model):
    image = models.ImageField(upload_to='gallery', verbose_name='Галлерея', blank=True, null=True)
    movie_id = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='gallery')

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фотки'


class NewsletterEmail(models.Model):
    email = models.EmailField(verbose_name='mail')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Reviews(models.Model):
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(verbose_name='Сообщение', max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(max_length=5000, verbose_name='Сообщение')
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.movie.title

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'





# Create your models here.
