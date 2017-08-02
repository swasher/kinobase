from django.conf import settings

import tmdbsimple as tmdb

from .models import Movie
from .models import Genre
from .models import Country



def fetch_tmdb_data(tmdbid, user):
    """

    :param tmdbid:
    :param user:
    :return: Объект типа Movie
    """
    tmdb.API_KEY = settings.TMDB_API_KEY
    moviedata = tmdb.Movies(tmdbid)
    response = moviedata.info(language='ru-RU')

    m, _ = Movie.objects.get_or_create(tmdbid=tmdbid, user=user)

    m.title = response['title']
    m.original_title = response['original_title']
    m.year = response['release_date'][:4]
    m.overview = response['overview']
    m.poster = response['poster_path']
    m.imdbid = response['imdb_id']
    if response['runtime']:
        m.runtime = int(response['runtime'])
    else:
        m.runtime = 0

    # countries = response.production_countries <class 'list'>: [{'name': 'United States of America', 'iso_3166_1': 'US'}]
    # genres = response.genres. Надо созадть таблицу жанров. genres возвращается так: <class 'list'>: [{'id': 12, 'name': 'приключения'}, {'id': 35, 'name': 'комедия'}, {'id': 10751, 'name': 'семейный'}, {'id': 878, 'name': 'фантастика'}]

    m.save()

    genres = response['genres']
    for genre in genres:
        g, _ = Genre.objects.get_or_create(tmdbid=genre['id'], name=genre['name'])
        m.genres.add(g)

    countries = response['production_countries']
    for country in countries:
        c, _ = Country.objects.get_or_create(name=country['name'])
        m.countries.add(c)

    return m