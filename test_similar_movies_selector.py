import pytest

from movie.views import get_random_similar_movies
from movie.models import KinopoiskMovie


@pytest.mark.django_db
def test_4_options():
    for _ in range(10_000):
        random_movie = KinopoiskMovie.objects.order_by('?').first()
        assert random_movie
        options = get_random_similar_movies(random_movie, amount=3)
        if len(options) != 3:
            print(random_movie)
        assert len(options) == 3
