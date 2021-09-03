import os
from random import shuffle

from django.db.models import Q
from django.shortcuts import render
from dotenv import load_dotenv
from pymongo import MongoClient

from movie.models import KinopoiskMovie

SPECIAL_GENRES = [
    'аниме',
    'мультфильм',
]

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']


def get_special_genre(movie, special_genres):
    return movie.genres.filter(name__in=special_genres).first()


def get_delta_by_year(year):
    if year <= 1955:
        return 20
    if 1955 < year < 1980:
        return 10
    if 1980 <= year < 2000:
        return 5
    if year >= 2000:
        return 3


def get_random_similar_movies(movie, amount=3):
    target_year = movie.year
    delta = get_delta_by_year(target_year)

    special_genre = get_special_genre(movie, SPECIAL_GENRES)

    if special_genre:
        delta *= 2

    min_year, max_year = target_year - delta, target_year + delta

    title_head = movie.title_ru[:4]
    exclude_target_movie = KinopoiskMovie.objects.exclude(title_ru__startswith=title_head)

    if special_genre:
        return exclude_target_movie\
            .filter(genres=special_genre)\
            .filter(Q(year__gt=min_year) & Q(year__lt=max_year))\
            .order_by('?')[:amount]

    return exclude_target_movie\
        .exclude(genres__name__in=SPECIAL_GENRES)\
        .filter(Q(year__gt=min_year) & Q(year__lt=max_year))\
        .order_by('?')[:amount]


def get_movie_and_options():
    random_movie = KinopoiskMovie.objects.order_by('?').first()
    options = get_random_similar_movies(random_movie)

    return random_movie, options


def index(request):
    if request.POST:
        client = MongoClient(MONGODB_URI)
        db = client['kekino']
        movie_stats = db['movie_stats']

        session_correct = request.session['correct']

        if not movie_stats.find_one({'_id': session_correct}):
            movie_stats.insert_one({'_id': session_correct, 'success': 0, 'fail': 0})

        if str(request.session.get('correct')) in request.POST:
            request.session['score'] += 1
            movie_stats.update_one({'_id': session_correct}, {'$inc': {'success': 1}})
        else:
            request.session['score'] = 0
            movie_stats.update_one({'_id': session_correct}, {'$inc': {'fail': 1}})

    if 'score' not in request.session:
        request.session['score'] = 0
    score = request.session['score']

    correct_answer, incorrect_answers = get_movie_and_options()
    request.session['correct'] = correct_answer.id
    options = [correct_answer, *incorrect_answers]
    shuffle(options)

    return render(request, 'index.html', {'options': options, 'score': score})
