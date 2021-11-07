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

        movies = movies_metadata['docs']

        for num, movie in enumerate(movies):
            print(num, movie['name'])

            kp_movie, _kp_movie_created = KinopoiskMovie.objects.update_or_create(
                kinopoisk_id=movie['id'],
                title_ru=movie['name'],
                title_en=str(movie.get('enName')),
                year=movie['year'],
            )
