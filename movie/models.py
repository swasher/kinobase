from django.db import models
from django.conf import settings


# ON DELETE CASCADE - вместе с данным объектом удаляются все объекты, внешние ключи которых указывают на данный объект.
class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    notice = models.TextField(blank=True, verbose_name='Заметка пользователя')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return str(self.tmdb_id)


class Tag(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    movie = models.ManyToManyField(Movie, blank=True)

    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'
        ordering = ['name']

    def __str__(self):
        return self.name
