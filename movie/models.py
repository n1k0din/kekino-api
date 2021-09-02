from django.db import models


class Country(models.Model):
    name = models.CharField('Название', max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=200)

    def __str__(self):
        return self.name


class KinopoiskMovie(models.Model):
    kinopoisk_id = models.PositiveIntegerField('Идентификатор фильма на Кинопоиске', db_index=True)
    title_ru = models.CharField('Название по-русски', max_length=500, db_index=True)
    title_en = models.CharField('Название по-английски', max_length=500, default='')
    year = models.PositiveSmallIntegerField('Год выпуска')

    countries = models.ManyToManyField(
        Country,
        related_name='country_movies',
        verbose_name='Страна',
    )

    genres = models.ManyToManyField(
        Genre,
        related_name='genre_movies',
        verbose_name='Жанры',
    )

    def __str__(self):
        return f'{self.title_ru}({self.title_en}), {self.year}'
