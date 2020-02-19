from django.urls import path
from movie import views
from movie import ajax

urlpatterns = [
    path('', views.hello, name='hello'),
    path('movie_detail/<int:pk>', views.movie_detail, name='movie_detail'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('movie_list/<str:tag>', views.movie_list, name='movie_list'),
    path('addmovie/<int:tmdbid>', views.addmovie, name='addmovie'),
    path('deletemovie/<int:pk>', views.deletemovie, name='deletemovie'),

    path('crew/<int:tmdbid>', views.crew, name='crew'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('search/', views.search, name='search'),
    path('updateinfo/<int:pk>', views.updateinfo, name='updateinfo'),

    path('notice_edit_ajax/', ajax.notice_edit_ajax, name='notice_edit_ajax'),

    path('tag_list/', views.tag_list, name='tag_list'),
    path('toggle_tag_ajax/', ajax.toggle_tag_ajax, name='toggle_tag_ajax'),
    path('delete_tag_ajax/', ajax.delete_tag_ajax, name='delete_tag_ajax'),
    path('create_tag_ajax/', ajax.create_tag_ajax, name='create_tag_ajax'),
    path('rename_tag_ajax/', ajax.rename_tag_ajax, name='rename_tag_ajax'),

    path('toggle_favorite_state/', ajax.toggle_favorite_state, name='toggle_favorite_state'),
    path('toggle_like_state/', ajax.toggle_like_state, name='toggle_like_state'),
    path('toggle_person/', ajax.toggle_person, name='toggle_person'),
]
