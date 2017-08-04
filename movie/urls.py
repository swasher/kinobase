from django.conf.urls import url
from movie import views
from movie import ajax

urlpatterns = [
    url(r'^$', views.hello, name='hello'),
    url(r'^movie_detail/(?P<pk>\d+)/$', views.movie_detail, name='movie_detail'),
    url(r'^movie_list/$', views.movie_list, name='movie_list'),
    url(r'^movie_list/(?P<tag>\d+)?$', views.movie_list, name='movie_list'),
    url(r'^addmovie/(?P<tmdbid>\d+)/$', views.addmovie, name='addmovie'),
    url(r'^deletemovie/(?P<pk>\d+)/$', views.deletemovie, name='deletemovie'),

    url(r'^crew/(?P<tmdbid>\d+)/$', views.crew, name='crew'),
    url(r'^cabinet/$', views.cabinet, name='cabinet'),
    url(r'^search/$', views.search, name='search'),
    url(r'^updateinfo/(?P<pk>\d+)/$', views.updateinfo, name='updateinfo'),

    url(r'^notice_edit_ajax/$', ajax.notice_edit_ajax, name='notice_edit_ajax'),

    url(r'^tag_list/$', views.tag_list, name='tag_list'),
    url(r'^toggle_tag_ajax/$', ajax.toggle_tag_ajax, name='toggle_tag_ajax'),
    url(r'^delete_tag_ajax/$', ajax.delete_tag_ajax, name='delete_tag_ajax'),
    url(r'^add_tag_ajax/$', ajax.create_tag_ajax, name='add_tag_ajax'),

    url(r'^toggle_favorite_state/$', ajax.toggle_favorite_state, name='toggle_favorite_state'),
    url(r'^toggle_like_state/$', ajax.toggle_like_state, name='toggle_like_state'),
    url(r'^toggle_person/$', ajax.toggle_person, name='toggle_person'),
]
