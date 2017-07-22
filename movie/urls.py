from django.conf.urls import url
from movie import views

urlpatterns = [
    url(r'^$', views.hello, name='hello'),
    url(r'^movie/(?P<tmdbid>\d+)/$', views.movie, name='movie'),


    url(r'^movies/$', views.movies, name='movies'),
    url(r'^movies/(?P<tag>\d+)?$', views.movies, name='movies'),

    url(r'^cabinet/$', views.cabinet, name='cabinet'),
    url(r'^search/$', views.search, name='search'),
    # #url(r'^add_movie/(?P<tmdb_id>\d+)/$', views.add_movie, name='add_movie'),
    url(r'^tags/$', views.tags, name='tags'),
    # url(r'^delete_movie/$', views.delete_movie, name='delete_movie'),
    url(r'^toggle_tag_ajax/$', views.toggle_tag_ajax, name='toggle_tag_ajax'),
    url(r'^delete_tag_ajax/$', views.delete_tag_ajax, name='delete_tag_ajax'),
    url(r'^add_tag_ajax/$', views.add_tag_ajax, name='add_tag_ajax'),
    url(r'^notice_edit_ajax/$', views.notice_edit_ajax, name='notice_edit_ajax'),
    url(r'^toggle_heart_state/$', views.toggle_heart_state, name='toggle_heart_state'),
    url(r'^toggle_like_state/$', views.toggle_like_state, name='toggle_like_state'),
]
