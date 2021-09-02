import json

from django.core.management.base import BaseCommand

from movie.models import Country, Genre, KinopoiskMovie


class Command(BaseCommand):
    help = 'Load movies from json file'

    def add_arguments(self, parser):
        parser.add_argument('movies_json_filename', nargs=1)

    def handle(self, *args, **options):
        filename = options['movies_json_filename'][0]

        with open(filename, encoding='utf-8') as f:
            movies_metadata = json.load(f)

        movies = movies_metadata['films']

        for movie in movies:
            print(movie['nameRu'])
            countries = []
            for country_name in movie['countries']:
                country, _country_created = Country.objects.get_or_create(name=country_name['country'])
                countries.append(country)

            genres = []
            for genre_name in movie['genres']:
                genre, _genre_created = Genre.objects.get_or_create(name=genre_name['genre'])
                genres.append(genre)

            kp_movie, _kp_movie_created = KinopoiskMovie.objects.update_or_create(
                kinopoisk_id=movie['filmId'],
                title_ru=movie['nameRu'],
                title_en=str(movie['nameEn']),
                defaults={
                    'year': movie['year'],
                }
            )

            for country in countries:
                kp_movie.countries.add(country)

            for genre in genres:
                kp_movie.genres.add(genre)
