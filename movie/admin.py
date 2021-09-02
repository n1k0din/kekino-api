from django.contrib import admin

from movie.models import Country, Genre, KinopoiskMovie

admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(KinopoiskMovie)
