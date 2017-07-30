from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import tmdbsimple as tmdb

from .models import Movie
from .models import Person


@receiver(post_save, sender=Movie)
def update_people(sender, instance, **kwargs):
    """
    У нас могут существовать персоны в таблице Persons, которые принимали участие в данном Movie.
    При создании Movie нужно создать m2m связи к этим персонам.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if kwargs['created']:
        # Если true - значит это только что созданный инстанс Movie

        tmdbid = instance.tmdbid
        user = get_user_model().objects.get(pk=instance.user_id)

        tmdb.API_KEY = settings.TMDB_API_KEY
        moviedata = tmdb.Movies(tmdbid)

        credits = moviedata.credits()

        # id всех Person для данного фильма
        crew = [k['id'] for k in credits['crew']]
        cast = [k['id'] for k in credits['cast']]
        movie_persons_id = list(set().union(crew, cast))

        # id всех Persons в моей базе данных
        stored_persons_id = list(Person.objects.filter(user=user).values_list('tmdbid', flat=True))

        # Находим все Person, которые есть и в объекте Movie и в таблице Persons
        persons = list(set(stored_persons_id) & set(movie_persons_id))
        # deprecated persons = list(set().union(stored_persons_id, movie_persons_id))

        for id in persons:
            p = Person.objects.get(tmdbid=id, user=user)
            instance.persons.add(p)