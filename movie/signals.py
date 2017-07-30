from django.db.models.signals import pre_init
from django.dispatch import receiver
from django.conf import settings

import tmdbsimple as tmdb

from .models import Movie


@receiver(pre_init, sender=Movie)
def update_people(sender, instance, **kwargs):
    """
    D vj
    У нас могут существовать персоны в таблице Persons, которые принимали участие в данном Movie.
    При создании Movie нужно создать m2m связи к этим персонам.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    tmdbid = instance.tmdbid

    tmdb.API_KEY = settings.TMDB_API_KEY
    moviedata = tmdb.Movies(tmdbid)

    credits = moviedata.credits()

    # id всех фильмов, в которых участвовал Person
    crew = [k['id'] for k in credits['crew']]
    cast = [k['id'] for k in credits['cast']]
    filmography_ids = list(set().union(crew, cast))

    # id всех фильмов в моей базе данных
    stored_ids = list(Movie.objects.filter(user=request.user).values_list('tmdbid', flat=True))

    # Находим все фильмы в базе с участием Person
    person_movies = list(set(stored_ids) & set(filmography_ids))

    for id in person_movies:
        m = Movie.objects.get(tmdbid=id)
        m.persons.add(p)