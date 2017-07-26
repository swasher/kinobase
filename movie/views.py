import datetime
from operator import itemgetter

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import tmdbsimple as tmdb

from .forms import MovieForm
from .models import Movie
from .models import Tag


def hello(request):
    return render(request, 'hello.html')


@login_required()
def cabinet(request):
    return render(request, 'cabinet.html')


@login_required
def search(request):

    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data['movie']

            tmdb.API_KEY = settings.TMDB_API_KEY

            c = tmdb.Configuration()
            """
            Example configuration info
            {
                'change_keys': ['adult', 'air_date', 'also_known_as', 'alternative_titles', 'biography', 'birthday', 'budget', 'cast', 'certifications', 'character_names', 'created_by', 'crew', 'deathday', 'episode', 'episode_number', 'episode_run_time', 'freebase_id', 'freebase_mid', 'general', 'genres', 'guest_stars', 'homepage', 'images', 'imdb_id', 'languages', 'name', 'network', 'origin_country', 'original_name', 'original_title', 'overview', 'parts', 'place_of_birth', 'plot_keywords', 'production_code', 'production_companies', 'production_countries', 'releases', 'revenue', 'runtime', 'season', 'season_number', 'season_regular', 'spoken_languages', 'status', 'tagline', 'title', 'translations', 'tvdb_id', 'tvrage_id', 'type', 'video', 'videos'],
                'images': {
                    'secure_base_url': 'https://image.tmdb.org/t/p/',
                    'profile_sizes': ['w45', 'w185', 'h632', 'original'],
                    'poster_sizes': ['w92', 'w154', 'w185', 'w342', 'w500', 'w780', 'original'],
                    'still_sizes': ['w92', 'w185', 'w300', 'original'],
                    'logo_sizes': ['w45', 'w92', 'w154', 'w185', 'w300', 'w500', 'original'],
                    'backdrop_sizes': ['w300', 'w780', 'w1280', 'original'],
                    'base_url': 'http://image.tmdb.org/t/p/'
                }
            }
            """
            configuration = c.info()
            base_url = configuration['images']['secure_base_url']
            poster_size = 'w185'
            prefix = base_url + poster_size

            search = tmdb.Search()
            response = search.movie(query=search_string, language='ru-RU')

            movies_unsorted = search.results
            movies = sorted(movies_unsorted, key=itemgetter('popularity'), reverse=True)
            """
            Example movie info 
            {
                'adult': False,
                'video': False,
                'overview': 'When a CIA operation to purchase classified Russian documents is blown by a rival agent, who then shows up in the sleepy seaside village where Bourne and Marie have been living. The pair run for their lives and Bourne, who promised retaliation should anyone from his former life attempt contact, is forced to once again take up his life as a trained assassin to survive.',
                'vote_average': 7.2,
                'poster_path': '/6a74OaZArLNNDHK9SdiLBUu2JYj.jpg',
                'backdrop_path': '/e1svWjxTXMOmdgkVLSPHSfWv90R.jpg',
                'genre_ids': [28, 18, 53],
                'release_date': '2004-07-23',
                'title': 'The Bourne Supremacy',
                'id': 2502,
                'vote_count': 2570,
                'popularity': 5.455147,
                'original_language': 'en',
                'original_title': 'The Bourne Supremacy'
            }
            """
    else:
        form = MovieForm()
        movies = None
        prefix = None

    return render(request, 'search.html', {'form':form, 'movies':movies, 'prefix':prefix})


@login_required
def movie(request, tmdbid):
    """
    Нужно понимать, что мы переменная moviedata, которая передается в темплейт, это dict, а не объект типа Movie,
    потому что у нас в базе не хранятся данные о фильмах.
    :param request:
    :param tmdbid: int, номер по tmdb.com
    :return: m         - объект db Movie (из него в темплейте нужны мой рейтинг, лайки и т.д)
             moviedata - объект Movies из tmdbsimple (данные о фильме)
    """

    tmdb.API_KEY = settings.TMDB_API_KEY
    moviedata = tmdb.Movies(tmdbid)
    response = moviedata.info(language='ru-RU')

    # TODO надо избавиться от частых вызовов (код в search) и либо обновлять эти, по сути, константы, изредка, или
    # вобще их в settings прописать
    base_url = 'http://image.tmdb.org/t/p/'
    poster_size = 'w500'
    prefix = base_url + poster_size

    m, _ = Movie.objects.get_or_create(tmdb_id=tmdbid, user=request.user)

    # Получаем список тегов, присвоенных данному фильму: <QuerySet ['tag2', 'tag5']>
    if Movie.objects.filter(tmdb_id=tmdbid).exists():
        active_tag_list = list(Tag.objects.filter(user=request.user, movie=m).values_list('name', flat=True))
    else:
        active_tag_list = []

    # Получаем список всех тегов от текущего юзера в виде списка словарей:
    # <QuerySet [{'active': 2, 'name': 'tag2', 'pk': 11}, {'active': 1, 'name': 'tag5', 'pk': 4}]>
    # Каждый кортеж содержит имя pk, имя тега и кол-во игр с данным тегом
    tag_list = Tag.objects \
        .filter(user=request.user) \
        .annotate(total=Count('movie')) \
        .values('pk', 'name', 'total')

    for tag in tag_list:
        if tag['name'] in active_tag_list:
            tag['active'] = True
        else:
            tag['active'] = False

    return render(request, 'movie.html', {'m':m, 'moviedata': moviedata, 'prefix': prefix, 'tag_list': tag_list})


# import asyncio
# from atmdb import TMDbClient
# async def get_movies(movies_paginator):
#     client = TMDbClient(api_token=settings.TMDB_API_KEY)
#     for m in movies_paginator.object_list:
#         movie = await client.get_movie(m['id'])
#         # assert movie.title == 'Fight Club'
#         title = movie.title
#         d = dict(['title', title])
#         m.update(d)
#     return movies_paginator


from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
@login_required
def movies(request, tag=None):
    base_url = 'http://image.tmdb.org/t/p/'
    poster_size = 'w154'
    prefix = base_url + poster_size

    user = request.user
    tags = Tag.objects.filter(user=request.user).annotate(total=Count('movie')).values('pk', 'name', 'total')

    # Если вьюха была вызвана пользователем путем нажатия на тэг, то ответ фильтруется по тэгу
    if tag:
        tag = int(tag)
        movie_list = Movie.objects.filter(user=user, tag__pk=tag)
    else:
        movie_list = Movie.objects.filter(user=user)

    # В базе у нас содержаться только ID, поэтому мы должны вытащить инфу из TMDB и уже ее передать в темплейт
    # Сначала создаем просто список по кол-ву всех фильмов у юзера, содержащий только tmdb_id
    tmdb_movies = []
    for m in movie_list:
        tmdb_movies.append(dict(id=m.tmdb_id))

    # Далее формируем пагинатор - ДО того, как вытаскивем инфу о фильмах, для уменьшения кол-ва запросов к TheMovieDB
    # Пагинатор работает у нас со списком фильмов, который еще не имеет никаких данных, кроме id
    paginator = Paginator(tmdb_movies, 12)  # Show N movies per page
    page = request.GET.get('page', 1)
    try:
        movies_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies_paginator = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies_paginator = paginator.page(paginator.num_pages)

    # После пагинации вытаскиваем из TMDB инфу только для фильмов, которые отобразятся на текущей странице пагинации
    """
    USING tmdbsimple
    """
    tmdb.API_KEY = settings.TMDB_API_KEY
    for m in movies_paginator.object_list:
        movie = tmdb.Movies(m['id'])
        response = movie.info(language='ru-RU')
        m.update(response)

    """
    USING atmdb
    aiohttp-2.2.3 async-timeout-1.2.1 atmdb-0.2.3 multidict-3.1.3 python-dateutil-2.6.1 yarl-0.12.0
    """
    #movies_paginator = get_movies(movies_paginator)

    # from atmdb import TMDbClient
    # client = TMDbClient(api_token=settings.TMDB_API_KEY)
    # for m in movies_paginator.object_list:
    #     movie = await client.get_movie(m['id'])
    #     #assert movie.title == 'Fight Club'
    #     title = movie.title
    #     d = dict(['title', title])
    #     m.update(d)

    return render(request, 'movies.html', {'movies': movies_paginator, 'prefix': prefix, 'tags':tags})



@login_required
@ensure_csrf_cookie
def delete_movie(request):
    """
    AJAX
    """
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        if 'movie_pk' in POST:
            pk = int(POST['game_pk'])

            # TODO тут у нас небольшой быдлокод:
            # except без укзания эксепшенов
            # при возникновении эксепшена статус failed никак не обрабатывается
            # можно, например, при неудачном удалении редирктить на страницу игры


            # # Сначала удаляем связь между игрой и юзером
            # #
            # try:
            #     game = Movie.objects.get(pk=pk)
            # except [Movie.DoesNotExist, Ownership.DoesNotExist]:
            #     pass
            #     #TODO возвратить на страницу игры
            # else:
            #     assigned_game.delete()
            #     messages.add_message(request, messages.INFO, "Game '{}' delete success".format(game.name))
            #
            #
            #
            # try:
            #     g = Game.objects.get(pk=pk)
            #     title = g.name
            #     Game.objects.get(pk=pk).delete()
            #     messages.add_message(request, messages.INFO, "Game '{}' delete success".format(title))
            # except:
            #     status = 'failed'
            # else:
            #     status = 'sucess'
            status = True
            results = {'redirect': '/movies/', 'status': status}
            return JsonResponse(results)


@login_required
def tags(request):
    tags = Tag.objects.filter(user=request.user).annotate(total=Count('movie')).values('pk', 'name', 'total')
    return render(request, 'tags.html', {'tags': tags})


@login_required
@ensure_csrf_cookie
def toggle_heart_state(request):
    """
    AJAX
    """
    results = {'status': 'error'}
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        if 'movie_pk' in POST:
            movie_pk = int(POST['movie_pk'])

            movie = Movie.objects.get(pk=movie_pk)
            state_after_click = movie.toggle_heart()

            if state_after_click:
                results = {'status': 'switch_on'}
            else:
                results = {'status': 'switch_off'}

    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def toggle_like_state(request):
    """
    AJAX
    """
    results = {'status': 'error'}
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        if 'movie_pk' in POST and 'button' in POST:
            movie_pk = int(POST['movie_pk'])
            button = str(POST['button'])

            movie = Movie.objects.get(pk=movie_pk)
            # state after click:
            like, dislike = movie.toggle_like(button)

            results = {'status':'success', 'like':like, 'dislike':dislike}

    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def notice_edit_ajax(request):
    """
    AJAX
    """
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        if 'movie_pk' in POST and 'text' in POST:
            movie_pk = int(POST['movie_pk'])
            text = str(POST['text'])
            try:
                movie = Movie.objects.get(pk=movie_pk)
                movie.notice = text
                movie.save()


                m = Movie.objects.get(pk=movie_pk)
                actual_text = m.notice
                results = {'status': 'sucess', 'actual_text': actual_text}

            except Exception as e:
                results = {'status': e}
            return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def toggle_tag_ajax(request):
    """
    AJAX
    """
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        if 'tag_pk' in POST and 'movie_pk' in POST:
            tag_pk = int(POST['tag_pk'])
            movie_pk = int(POST['movie_pk'])
            tag = Tag.objects.get(pk=tag_pk)

            if not Movie.objects.filter(pk=movie_pk).exists():
                m = Movie()
                m.tmdb_id = movie_pk
                m.user = request.user
                m.save()

            movie = Movie.objects.get(pk=movie_pk)

            if Tag.objects.filter(pk=tag_pk, movie__pk=movie.pk).exists():
                tag.movie.remove(movie)
                results = {'status': 'sucess_remove'}
                return JsonResponse(results)
            else:
                tag.movie.add(movie)
                results = {'status': 'sucess_add'}
                return JsonResponse(results)

            # todo Здесь можно запились функцию, проверяющую - если у фильма
            # не осталось ни тэгов ни звезд - удалить его из базы


@login_required
@ensure_csrf_cookie
def delete_tag_ajax(request):
    """
    AJAX
    """
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        results = {}
        tag_name = 'default'

        if 'tagpk' in POST:
            tagpk = int(POST['tagpk'])

            try:
                tag = Tag.objects.get(pk=tagpk)
                tag_name = tag.name
                if not Movie.objects.filter(tag=tag).exists():
                    #messages.add_message(request, messages.INFO, "Tag `{}` delete success".format(tag_name))
                    #messages.success(request, "The object has been modified.")
                    tag.delete()
                    status = 'sucess'
                else:
                    #messages.add_message(request, messages.INFO, "Tag `{}` has movies!".format(tag_name))
                    #messages.error(request, "The object was not modified.")
                    status = 'exist'
            except:
                status = 'failed'

            results = {'status': status, 'name': tag_name,
                       #'messages':django_messages
                       }

        return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def add_tag_ajax(request):
    """
    AJAX
    """
    # if request.is_ajax() and request.method == u'POST':
    if request.method == u'POST':
        POST = request.POST
        tagpk = None
        results = {}

        if 'tag_name' in POST:
            tag_name = str(POST['tag_name'])

            try:
                if not Tag.objects.filter(name=tag_name).exists():
                    tag = Tag.objects.create(name=tag_name, user=request.user)
                    tag.save()
                    # messages.add_message(request, messages.INFO, 'tag {} creating success'.format(tag_name))
                    status = 'sucess'
                    tagpk = tag.pk
                else:
                    # messages.add_message(request, messages.WARNING, 'tag {} already exist'.format(tag_name))
                    status = 'exist'
            except:
                status = 'failed'

            results = {'status': status, 'name': tag_name, 'tagpk': tagpk}

            return JsonResponse(results)

    else:
        results = {'status': 'non-ajax', 'name': None}
        return JsonResponse(results)