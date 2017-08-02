from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


class Genre(models.Model):
    tmdbid = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# {'order': 1, 'profile_path': '/4d4wvNyDuvN86DoneawbLOpr8gH.jpg', 'gender': 1, 'credit_id': '52fe4c56c3a368484e1b31ab',
# 'id': 4491, 'cast_id': 8, 'name': 'Jennifer Aniston', 'character': "Rose O'Reilly"}
class Person(models.Model):
    """
    Логика такая.
    - Мы НЕ храним информацию о том, в роли кого выступал человек в конкретном фильме (актер, режиссер, и тд)
    - Люди, которые хранятся в этой таблице, по сути являются favorite (отмеченными лайком)
    - Когда добавляется новый фильм в коллекцию, или нажимается update, производится сравнение всех favorite с теми, кто в фильме, и добавляются связи many-to-many
    - Когда мы открывыаем страницу фильма, мы сразу видим кто из favorite принимал в нем участие
    - По нажитию на кнопку - появляются все актеры и команда, и мы можем кого-то из них добавить в favorite
    - Лица на странице Фильма отображаются из локальной базы, на странице People - делается реквест на tmdb

    """
    tmdbid = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=30)
    face = models.CharField(max_length=128, blank=True, verbose_name='часть url\'a для постера')  # like '/4d4wvNyDuvN86DoneawbLOpr8gH.jpg'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        unique_together = ("tmdbid", "user")


# ON DELETE CASCADE - вместе с данным объектом удаляются все объекты, внешние ключи которых указывают на данный объект.
class Movie(models.Model):
    tmdbid = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    notice = models.TextField(blank=True, verbose_name='Заметка пользователя')
    genres = models.ManyToManyField(Genre)
    countries = models.ManyToManyField(Country)
    persons = models.ManyToManyField(Person)

    # five predefined 'tags'
    like = models.BooleanField(default=False, verbose_name='Лайк') # Может быть включен только один из Like-Dislike.
    dislike = models.BooleanField(default=False, verbose_name='Дизлайк') # Это регулируется в сигналах и рисуется через jQuery
    favorite = models.BooleanField(default=False, verbose_name='Любимый фильм')
    watched = models.BooleanField(default=False, verbose_name='Просмотрено')
    planned = models.BooleanField(default=False, verbose_name='Буду смотреть')

    title = models.CharField(max_length=128, blank=True, verbose_name='Название на русском')
    original_title = models.CharField(max_length=128, blank=True, verbose_name='Название на языке оригинала')
    year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Год выпуска')
    overview = models.TextField(blank=True, null=True)
    poster = models.CharField(max_length=128, blank=True, verbose_name='часть url\'a для постера')
    runtime = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Продолжительность в минутах')
    imdbid = models.CharField(max_length=16, blank=True, null=True, verbose_name='id на imdb')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        unique_together = ("tmdbid", "user")

    def __str__(self):
        return '{} [owner {}]'.format(self.title, self.user.email)

    def toggle_favorite(self):
        self.favorite = not self.favorite
        self.save()
        return self.favorite

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

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.pk)])


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