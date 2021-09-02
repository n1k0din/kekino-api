from django.shortcuts import render
from django.db.models import Q

from movie.models import KinopoiskMovie


def get_delta_by_year(year):
    if year < 1950:
        return 16
    if 1950 <= year < 1980:
        return 8
    if 1980 <= year < 2000:
        return 4
    if year >= 2000:
        return 2


def get_random_similar_movies(movie, amount=3):
    target_year = movie.year
    delta = get_delta_by_year(target_year)
    min_year, max_year = target_year - delta, target_year + delta

    options = KinopoiskMovie.objects\
        .exclude(id=movie.id)\
        .filter(Q(year__gt=min_year) & Q(year__lt=max_year))\
        .order_by('?')[:amount]

    return options


def get_movie_and_options():
    random_movie = KinopoiskMovie.objects.order_by('?').first()
    options = get_random_similar_movies(random_movie)

    return random_movie, options


def index(request):
    correct_answer, incorrect_answers = get_movie_and_options()
    options = [correct_answer, *incorrect_answers]

    return render(request, 'index.html', {'options': options})
