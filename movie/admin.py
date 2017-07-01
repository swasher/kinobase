from django.contrib import admin
from .models import Movie


admin.site.site_header = 'Private Cinema'

admin.site.register(Movie)
