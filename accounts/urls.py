from django.conf.urls import url, include
from django.contrib import auth
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # # url(r'^login/(?P<next>\w+)/$', views.login, name='login'),
    # # url(r'^logout/$', views.logout, name='logout'),

    #url(r'^user_registration/$', views.user_registration, name='user_registration'),
    #url(r'^user_login/$', views.user_login, name='user_login'),
    # url(r'^accounts/login/$', auth.views.login, {'template_name': 'registration/login.html'}),
    #url(r'^accounts/', include('registration.backends.hmac.urls')),
    #url(r'^login/$', auth_views.login),


]