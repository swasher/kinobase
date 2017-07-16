from django.contrib import admin
from .models import Movie
from .models import Tag


admin.site.site_header = 'Private Cinema'

admin.site.register(Movie)
admin.site.register(Tag)
