import json
import os

import requests
from django.conf import settings
from django.core.management import BaseCommand

from website.helpers import gen_datetime
from website.models import (
    Actor,
    Genre,
    Movie,
    MovieGallery,
    Category
)


def get_digits(item):
    """
    Получаем только числа из строки
    :param item: строка из которой нужно забрать числа
    :return: возвращаем целое число полученное из строки
    """
    if isinstance(item, int):  # проверка на то, является ли объект типом данных int
        return item  # если да, то отдаем сразу значение

    # если нет, то через filter и lambda получаем список только тех символов, которые являются числом
    # полученный список строк склеиваем в строку, получаем строку, где все символы являются цифрой
    # меняем тип данных на int
    return int(''.join(list(filter(lambda x: x.isdigit(), item))))


def get_file_bytes(file_url: str):
    """
    Получаем байты фотографии хранящейся где-то в интернете

    :param file_url: ссылка до файла, на которую отправляем запрос и получаем данные в байтах
    :return: возвращаем байты данной ссылки после отправленного запроса
    """
    return requests.get(file_url).content


def create_folders():
    """
    Создаем нужные папки, где будут храниться фотографии
    :return: None
    """

    # проверяем есть ли в проекте папка 'media'
    is_media_exists = os.path.exists(settings.MEDIA_ROOT)

    # проверяем есть ли в внутри у папки 'media' папки 'movies' и 'previews'
    # это те папки, где будут храниться фото, добавленные для поля poster
    is_previews_folder_exists = os.path.exists(os.path.join(settings.MEDIA_ROOT, 'movies', 'previews'))

    if not is_media_exists:  # если нет папки 'media', то создаем ее
        os.mkdir(settings.MEDIA_ROOT)

    if not is_previews_folder_exists:  # если нет папкок 'movies' и 'previews', то создаем их
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'movies', 'previews'))


def save_poster_image(image_url: str):
    """
    Сохраняем фото по ссылке, в папку для хранения постеров
    :param image_url: Ссылка до фотографии которую хотим добавить в поле poster у модели Movie
    :return: None
    """
    create_folders()  # создаем нужные папки для фоток
    content = get_file_bytes(image_url)  # получаем байты фотографии по ссылке
    image_name = image_url.split('/')[-1]  # получаем название фотографии для сохранения

    # открываем папки и файл на запись байтов и сохраняем байты фотографии как отдельный файл в нужную папку
    with open(os.path.join(settings.MEDIA_ROOT, 'movies', 'previews', image_name), 'wb') as f:
        f.write(content)


def save_gallery_images(movie: Movie, images_urls: list[str]):
    """
    Сохраняем фотки из списка ссылок на фотографии связанные с фильмом
    :param movie: объект модели Movie
    :param images_urls: список ссылок для записи
    :return: None
    """

    # проверяем существует ли путь до папки где будут храниться фотки определенного фильма
    # movie.slug - название папки, которая берет свое названия из поля slug у фильма
    # чтобы фотки для определенного фильма хранились в отдельной папке а не в одной
    is_gallery_folder_exists = os.path.exists(
        os.path.join(settings.MEDIA_ROOT, 'movies', 'gallery', movie.slug)
    )

    # если путь до папки не найден, то создаем эти папки
    if not is_gallery_folder_exists:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'movies', 'gallery', movie.slug))

    for image_url in images_urls:  # цикл по списку ссылок на фотографии
        image_name = image_url.split('/')[-1]  # получаем название фотографии из ссылки

        # сохраняем и создаем файл с полученным названием в папке отведенной для фильма
        with open(os.path.join(settings.MEDIA_ROOT, 'movies', 'gallery', movie.slug, image_name), 'wb') as f:
            content = get_file_bytes(image_url)
            f.write(content)

# python manage.py
class Command(BaseCommand):
    help = 'Загружаем фильмы из json файла'

    def handle(self, *args, **options):

        # открываем json файл для работы с полученными данными
        with open('movies.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)  # загружаем все данные из файла в переменную

            # пробегаемся в цикле по полученному списку словарей
            # enumerate - дает возможность получить самоу значение и сделать для него нумерацию, которая начинается с 0
            for idx, item in enumerate(data):
                # title = item['title'].split('.')[-1].strip()  # получаем название файла избавляя его от ненужного
                # budget = get_digits(item['budget'])  # получаем целое число из ключа budget
                # fees_usa = get_digits(item['fees_usa'])  # получаем целое число из ключа fees_usa
                # fees_world = get_digits(item['fees_world'])  # получаем целое число из ключа fees_world
                # image_name = item['poster'].split('/')[-1].strip()  # получаем название фотографии из ключа poster
                #
                # if idx <= 8:  # если счетчик меньше либо равен 8 то получаем категорию Фильмы
                #     category = Category.objects.get(title='Фильмы')
                # else:  # если больше 8, то Сериалы
                #     category = Category.objects.get(title='Сериалы')
                #
                # date = gen_datetime(min_year=int(item['year']))  # генерируем случайную дату по году выпуска фильма
                #
                # # создаем новый объект для модели Movie
                # movie_obj = Movie(
                #     title=title,
                #     slogan='slogan',  # дефолтное значение которое будет у всех фильмов
                #     budget=budget,
                #     poster=os.path.join('movies', 'previews', image_name),  # получаем строку с абсолютным путем до файла
                #     fees_usa=fees_usa,
                #     fees_world=fees_world,
                #     category=category,
                #     premier_date=date,
                #     year=int(item['year']),
                #     producer=item['producer'],
                #     country=item['country'],
                #     rating=float(item['rating']),
                #     description=item['description'],
                # )
                # movie_obj.save()
                save_poster_image(item['poster'])

                # photos list
                # photos = item['photos']  # получаем список ссылок фотографий
                # save_gallery_images(movie_obj, images_urls=photos)  # создаем данные фотографии в папке media
                # for photo in photos:
                #     # добавляем новую запись в таблицу MovieGallery
                #     gallery_obj = MovieGallery(
                #         movie_id=movie_obj,  # ссылаемся на определенный фильм
                #         image=os.path.join('movies', 'gallery', movie_obj.slug, photo.split('/')[-1]),  # путь до фото
                #     )
                #     gallery_obj.save()
                #
                # # genres list
                # genres = item['genre']  # список жанров
                # for genre in genres:
                #     if not Genre.objects.filter(title=genre).exists():  # проверяем если нет жанра, чтобы не было дубликатов
                #         obj = Genre(title=genre)
                #         obj.save()  # создаем жанк
                #     genre_obj = Genre.objects.get(title=genre)  # получаем жанр по его названию
                #     movie_obj.genre.add(genre_obj)  # добавляем в фильм
                #
                # # actors list
                # actors = item['actors']
                # for actor in actors:
                #     obj = Actor(fullname=actor, movie_id=movie_obj)
                #     obj.save()
