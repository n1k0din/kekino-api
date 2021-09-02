from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from movie import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index)
    # path('movie/', include('movie.urls')),
]
