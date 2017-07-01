import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import MovieForm
from .models import Movie


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


    else:
        form = MovieForm()
        response = None

    return render(request, 'search.html', {'form':form, 'movies':response})


@login_required
def movies(request):
    user = request.user

    if 'filter' in request.GET and request.GET['filter'] == 'tag':
        movie_list = Movie.objects.filter(user=user, tag__pk=request.GET['pk'])
    else:
        movie_list = Movie.objects.filter(user=user)

    paginator = Paginator(movie_list, 8)  # Show 6 movies per page
    page = request.GET.get('page', 1)

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies = paginator.page(paginator.num_pages)

    return render(request, 'movies.html', {'movies': movies})


#
# DEPRECATED
# Не надо никаого add!!! Когда юзер добавляет фильм в список, он должен автоматически "добавляться"
#
@login_required
@ensure_csrf_cookie
def add_movie(request, igdb_id):

    if not Movie.objects.filter(igdb_id=igdb_id).exists():

        movie = Movie()
        movie.igdb_id = igdb_id
        movie.user = request.user
        movie.date_add = datetime.datetime.now()
        movie.save()

    return redirect('/game/{}'.format(movie.id))


@login_required
def movie(request, pk):
    movie = Movie.objects.get(pk=pk)

    # Получаем список тегов, присвоенных данной игре: <QuerySet ['tag2', 'tag5']>
    # active_tag_list = list(Tag.objects\
    #     .filter(user=request.user, games=game)\
    #     .values_list('name', flat=True))
    #     # .values_list('name', 'active')
    #     # .annotate(active=Count('games'))\

    # tag_list = Tag.objects\
    #     .filter(user=request.user) \
    #     .annotate(total=Count('games'))\
    #     .values('pk', 'name', 'total')
    #
    # for tag in tag_list:
    #     if tag['name'] in active_tag_list:
    #         tag['active'] = True
    #     else:
    #         tag['active'] = False

    return render(request, 'movie.html', {'movie': movie,
                                          #'tags': tag_list
                                          })



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


# @login_required
# def tags(request):
#     tag_list = Tag.objects.all().filter(user=request.user)
#     return render(request, 'tags.html', {'tags': tag_list})


# @login_required
# @ensure_csrf_cookie
# # AJAX
# def toggle_tag(request):
#     if request.is_ajax() and request.method == u'POST':
#         POST = request.POST
#         if 'tag_pk' in POST and 'game_pk' in POST:
#             tag_pk = int(POST['tag_pk'])
#             game_pk = int(POST['game_pk'])
#             tag = Tag.objects.get(pk=tag_pk)
#             game = Game.objects.get(pk=game_pk)
#
#             if Tag.objects.filter(games=game, pk=tag_pk).exists():
#                 tag.games.remove(game)
#                 results = {'status': 'sucess_remove'}
#                 return JsonResponse(results)
#             else:
#                 tag.games.add(game)
#                 results = {'status': 'sucess_add'}
#                 return JsonResponse(results)

# @login_required
# @ensure_csrf_cookie
# def delete_tag_ajax(request):
#     """
#     AJAX
#     """
#     if request.is_ajax() and request.method == u'POST':
#         POST = request.POST
#         results = {}
#         tag_name = 'default'
#
#         if 'pk' in POST:
#             pk = int(POST['pk'])
#
#             try:
#                 tag = Tag.objects.get(pk=pk)
#                 tag_name = tag.name
#                 if not Game.objects.filter(tag=tag).exists():
#                     messages.add_message(request, messages.INFO, "Tag `{}` delete success".format(tag_name))
#                     #messages.success(request, "The object has been modified.")
#                     tag.delete()
#                     status = 'sucess'
#                 else:
#                     messages.add_message(request, messages.INFO, "Tag `{}` has games!".format(tag_name))
#                     #messages.error(request, "The object was not modified.")
#                     status = 'exist'
#             except:
#                 status = 'failed'
#
#             results = {'status': status, 'name': tag_name}
#
#         return JsonResponse(results)


# @login_required
# @ensure_csrf_cookie
# def add_tag_ajax(request):
#     """
#     AJAX
#     """
#     # if request.is_ajax() and request.method == u'POST':
#     if request.method == u'POST':
#         POST = request.POST
#         tagpk = None
#         results = {}
#
#         if 'tag_name' in POST:
#             tag_name = str(POST['tag_name'])
#
#             try:
#                 if not Tag.objects.filter(name=tag_name).exists():
#                     tag = Tag.objects.create(name=tag_name, user=request.user)
#                     tag.save()
#                     messages.add_message(request, messages.INFO, 'tag {} creating success'.format(tag_name))
#                     status = 'sucess'
#                     tagpk = tag.pk
#                 else:
#                     messages.add_message(request, messages.WARNING, 'tag {} already exist'.format(tag_name))
#                     status = 'exist'
#             except:
#                 status = 'failed'
#
#             results = {'status': status, 'name': tag_name, 'tagpk': tagpk}
#
#             return JsonResponse(results)
#
#     else:
#         results = {'status': 'non-ajax', 'name': None}
#         return JsonResponse(results)