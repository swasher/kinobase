from django.conf.urls import url
from movie import views

urlpatterns = [
    url(r'^$', views.hello, name='hello'),
    url(r'^movie/(?P<pk>\d+)/$', views.movie, name='movie'),
    url(r'^movies/$', views.movies, name='movies'),
    url(r'^cabinet/$', views.cabinet, name='cabinet'),
    url(r'^search/$', views.search, name='search'),
    # #url(r'^add_movie/(?P<tmdb_id>\d+)/$', views.add_movie, name='add_movie'),
    # url(r'^tags/$', views.tags, name='tags'),
    # url(r'^toggle_tag/$', views.toggle_tag, name='toggle_tag'),
    # url(r'^delete_movie/$', views.delete_movie, name='delete_movie'),
    # url(r'^delete_tag_ajax/$', views.delete_tag_ajax, name='delete_tag_ajax'),
    # url(r'^add_tag_ajax/$', views.add_tag_ajax, name='add_tag_ajax'),
]
