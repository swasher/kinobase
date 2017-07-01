from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager


# ON DELETE CASCADE - вместе с данным объектом удаляются все объекты, внешние ключи которых указывают на данный объект.
class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    notice = models.TextField(blank=True, verbose_name='Заметка пользователя')
    tags = TaggableManager()


    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return str(self.tmdb_id)

