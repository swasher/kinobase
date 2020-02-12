# Place for ajax views
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings

import tmdbsimple as tmdb

from .models import Tag
from .models import Movie
from .models import Person


@login_required
def toggle_person(request):
    """
    AJAX
    """
    status = None
    error_code = None

    if request.method == u'POST':
        POST = request.POST

        if 'person_tmdbid' in POST:
            person_tmdbid = str(POST['person_tmdbid'])

            try:
                if Person.objects.filter(tmdbid=person_tmdbid, user=request.user).exists():
                    p = Person.objects.get(tmdbid=person_tmdbid, user=request.user)
                    p.delete()
                    status = 'deleted'
                else:
                    tmdb.API_KEY = settings.TMDB_API_KEY
                    person = tmdb.People(person_tmdbid)
                    response = person.info()

                    p = Person()
                    p.user = request.user
                    p.tmdbid = int(response['id'])
                    p.name = response['name']
                    p.face = response['profile_path']
                    p.save()

                    # После того, как User добавил в свою коллекцию нового Person, нужно создать
                    # m2m связи для всех фильмов, где он принимал участие. Тогда на странице movie_detail мы видим
                    # связанных с фильмом людей.
                    #
                    # Делается это так -
                    # сначала для Person забираются данные о его фильмах с themoviedb (person.movie_credits()),
                    # затем создаются два списка - id фильмов для Person (filmography_ids) и id всех фильмов User'а (stored_ids),
                    # вычисяляется пересечение этих списков (union), и по этому пересечению устанавливаются связи m2m.
                    response = person.movie_credits()

                    # id всех фильмов, в которых участвовал Person
                    crew = [k['id'] for k in response['crew']]
                    cast = [k['id'] for k in response['cast']]
                    filmography_ids = list(set().union(crew, cast))

                    # id всех фильмов в моей базе данных
                    stored_ids = list(Movie.objects.filter(user=request.user).values_list('tmdbid', flat=True))

                    # Находим все фильмы в базе с участием Person (получаем список id)
                    person_movies = list(set(stored_ids) & set(filmography_ids))

                    for id in person_movies:
                        m = Movie.objects.get(tmdbid=id, user=request.user)
                        m.persons.add(p)

                    status = 'in_database'
            except Exception as e:
                status = 'failed'
                error_code = '{}'.format(e)

    else:
        status = 'non-ajax'

    results = {'status': status, 'error_code': error_code}
    return JsonResponse(results)


@login_required
@ensure_csrf_cookie
def create_tag_ajax(request):
    """
    AJAX
    """
    print('create_tag_ajax')
    message = ''
    tagpk = None
    name = ''

    if request.method == u'POST' and 'tag_name' in request.POST:
        tag_name = str(request.POST['tag_name'])

        if tag_name: # если тег не пустой
            if not Tag.objects.filter(name=tag_name).exists():
                tag = Tag.objects.create(name=tag_name, user=request.user)
                tag.save()
                success = True
                tagpk = tag.pk
                name = tag.name
            else:
                success = False
                message = 'tag already exist'
        else:
            success = False
            message = "Can't create empty tag"
    else:
        success = False
        message = 'non-ajax'

    results = {'success': success, 'message': message, 'name': name, 'tagpk': tagpk}
    return JsonResponse(results)


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
                    # messages.add_message(request, messages.INFO, "Tag `{}` delete success".format(tag_name))
                    # messages.success(request, "The object has been modified.")
                    tag.delete()
                    status = 'sucess'
                else:
                    # messages.add_message(request, messages.INFO, "Tag `{}` has movies!".format(tag_name))
                    # messages.error(request, "The object was not modified.")
                    status = 'exist'
            except:
                status = 'failed'

            results = {'status': status, 'name': tag_name,
                       # 'messages':django_messages
                       }

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

            # if not Movie.objects.filter(pk=movie_pk).exists():
            #     m = Movie()
            #     m.tmdbid = movie_pk
            #     m.user = request.user
            #     m.save()

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
def toggle_favorite_state(request):
    """
    AJAX
    """
    results = {'status': 'error'}
    if request.is_ajax() and request.method == u'POST':
        POST = request.POST
        if 'movie_pk' in POST:
            movie_pk = int(POST['movie_pk'])

            movie = Movie.objects.get(pk=movie_pk)
            state_after_click = movie.toggle_favorite()

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

            results = {'status': 'success', 'like': like, 'dislike': dislike}

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