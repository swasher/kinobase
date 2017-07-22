from django.db import models
from django.conf import settings


# ON DELETE CASCADE - вместе с данным объектом удаляются все объекты, внешние ключи которых указывают на данный объект.
class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    notice = models.TextField(blank=True, verbose_name='Заметка пользователя')
    like = models.BooleanField(default=False, verbose_name='Лайк') # Может быть включен только один из Like-Dislike.
    dislike = models.BooleanField(default=False, verbose_name='Дизлайк') # Это регулируется в сигналах и рисуется через jQuery
    heart = models.BooleanField(default=False, verbose_name='Любимый фильм') #

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return 'Movie with tmdbid: '.format(self.tmdb_id)

    def toggle_heart(self):
        self.heart = not self.heart
        self.save()
        return self.heart

    def toggle_like(self, field):
        # Есть две кнопки - LIKE и DISLIKE. Включение одной выключает другую.
        # Если при этом другая уже была выключена, она не меняется.
        # Выключение (on->off) одной не меняет состояние другой.
        if field == 'like':
            self.like = not self.like
            if self.like:
                self.dislike = False

        elif field == 'dislike':
            self.dislike = not self.dislike
            if self.dislike:
                self.like = False

        else:
            raise ValueError('Unknown button name')

        self.save()

        return self.like, self.dislike


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
