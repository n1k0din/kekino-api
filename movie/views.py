from django.shortcuts import render

from movie.models import KinopoiskMovie


def index(request):
    random_movie = KinopoiskMovie.objects.order_by('?').first()

    options = KinopoiskMovie.objects.exclude(id=random_movie.id).filter().order_by('?')[:3]

    context = {
        'movie': random_movie,
        'options': options,
    }


    return render(request, 'index.html', context)
