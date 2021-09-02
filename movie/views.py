from django.shortcuts import render
from django.db.models import Q

from movie.models import KinopoiskMovie


def get_random_similar_movies(movie, amount=3, delta_years=7):
    target_year = movie.year
    min_year, max_year = target_year - delta_years, target_year + delta_years

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
