import pytest

from movie.views import get_random_similar_movies
from movie.models import KinopoiskMovie


@pytest.mark.django_db
def test_4_options():
    movies = KinopoiskMovie.objects.all()
    for movie in movies:
        options = get_random_similar_movies(movie, amount=3)
        if len(options) != 3:
            print(movie)
        assert len(options) == 3
