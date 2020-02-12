import datetime
from operator import itemgetter
from itertools import groupby

from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page

import tmdbsimple as tmdb

from .forms import MovieForm
from .models import Movie
from .models import Tag
from .models import Person
from .util import fetch_tmdb_data


def hello(request):
    return render(request, 'hello.html')


@login_required()
def cabinet(request):
    return render(request, 'cabinet.html')


@login_required
def search(request):
    moviesdata = None
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data['movie']
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

            tmdb.API_KEY = settings.TMDB_API_KEY
            search = tmdb.Search()
            response = search.movie(query=search_string, language='ru-RU')

            movies_unsorted = search.results
            moviesdata = sorted(movies_unsorted, key=itemgetter('popularity'), reverse=True)
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

    return render(request, 'search.html', {'form':form, 'moviesdata': moviesdata})


@login_required
def person_list(request):
    persons = Person.objects.filter(user=request.user)
    return render(request, 'person_list.html', {'persons': persons})


@login_required
def updateinfo(request, pk):
    """
    Повторный забор данных с themoviedb.com для уже существующего фильма.
    :param request:
    :param pk:
    :return:
    """
    m = Movie.objects.get(pk=pk)
    fetch_tmdb_data(m.tmdbid, request.user)
    return redirect(m)


@login_required
def crew(request, tmdbid):

    m = Movie.objects.get(tmdbid=tmdbid, user=request.user)
    title = '{} [{}]'.format(m.title, m.year)

    tmdb.API_KEY = settings.TMDB_API_KEY
    moviedata = tmdb.Movies(tmdbid)

    credits = moviedata.credits()
    cast = credits['cast']
    crew = credits['crew']
    # cast
    # {'character': 'Nikander', 'credit_id': '52fe420dc3a36847f8000087', 'gender': 2, 'cast_id': 5, 'id': 4826, 'order': 0, 'name': 'Matti Pellonpää', 'profile_path': '/7WuLvkuWphUAtW6QQwtF3WrwUKE.jpg'}
    # crew
    # {'job': 'Screenplay', 'department': 'Writing', 'profile_path': '/8nQcTzKUmRh6MPprd1n6iOauYPf.jpg', 'gender': 0, 'credit_id': '52fe420dc3a36847f8000077', 'id': 16767, 'name': 'Aki Kaurismäki'}


    # Наборы crew может содержать несколько вхождений на одного человека, например, человек был и директором,
    # и писателем, и оператором. Этот цикл объеденяет такие записи.
    # sorted = sorted(d, key=lambda k: k['id'])
    actors_combined_by_job = []
    for key, group in groupby(crew, lambda x: x['id']):
        # в каждом цикле - key - это 'id' словаря, а group - это итератор, содержащий все словари с данным id
        all_actor_jobs = list(group)
        j = all_actor_jobs[0]
        j['job'] = '<br>'.join([k['job'] for k in all_actor_jobs])
        actors_combined_by_job.append(j)

    crew = actors_combined_by_job

    # Имеющихся в таблице Person людей помечаем, чтобы обозначить их в темплейте (зеленой рамкой)
    actors_in_db = list(Person.objects.filter(user=request.user).values_list('tmdbid', flat=True))
    for actor in cast:
        if actor['id'] in actors_in_db:
            actor['stored'] = True
    for actor in crew:
        if actor['id'] in actors_in_db:
            actor['stored'] = True

    return render(request, 'movie_crew.html', {'cast': cast, 'crew':crew, 'title':title })


@login_required
def movie_detail(request, pk):
    """
    :param request:
    :param tmdbid:     - id по tmdb. Передается именно он, а не Movie.pk, так как данного фильма может еще не быть в базе,
                         и тогда его нужно сначала создать.
    :return: movie     - объект Movie
    """
    movie = Movie.objects.get(pk=pk)

    # Получаем список тегов, присвоенных данному фильму: <QuerySet ['tag2', 'tag5']>
    active_tag_list = list(Tag.objects.filter(user=request.user, movie=movie).values_list('name', flat=True))

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

    return render(request, 'movie_detail.html', {'movie': movie, 'tag_list': tag_list})


#@cache_page(60 * 5)
@login_required
def movie_list(request, tag=None):
    user = request.user
    get = request.GET

    movie_list = Movie.objects.filter(user=user)

    filters = ['country', 'genre']
    sortings = ['title', 'year', 'runtime', ]
    for key, value in request.GET.items():
        if key in filters:
            # add_filter(k, v)
            pass
        if key in sortings:
            movie_list = movie_list.order_by(value)

    # Если вьюха была вызвана пользователем путем нажатия на тэг, то ответ фильтруется по тэгу
    if tag:
        tag = int(tag)
        movie_list = Movie.objects.filter(user=user, tag__pk=tag)
    else:
        movie_list = Movie.objects.filter(user=user)


    # products = Product.objects.all()
    # order = request.GET.get('order', 'name')  # Set 'name' as a default value
    # products = products.order_by(order)
    # return render(request, 'products_list.html', {
    #     'products': products
    # })

    tags = Tag.objects.filter(user=request.user).annotate(total=Count('movie')).values('pk', 'name', 'total')

    paginator = Paginator(movie_list, 15)  # Show N movies per page
    page = request.GET.get('page', 1)
    try:
        movies_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies_paginator = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies_paginator = paginator.page(paginator.num_pages)

    return render(request, 'movie_list.html', {'movies': movies_paginator, 'tags':tags})


@login_required
def tag_list(request):
    tags = Tag.objects.filter(user=request.user).annotate(total=Count('movie')).values('pk', 'name', 'total')
    return render(request, 'tag_list.html', {'tags': tags})


@login_required
def addmovie(request, tmdbid):
    if not Movie.objects.filter(tmdbid=tmdbid, user=request.user).exists():
        fetch_tmdb_data(tmdbid, request.user)

    movie = Movie.objects.get(tmdbid=tmdbid, user=request.user)
    return redirect(movie)


@login_required
def deletemovie(request, pk):
    m = Movie.objects.get(pk=pk)
    m.delete()
    return redirect('movie_list')