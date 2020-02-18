from django.contrib import admin
from .models import Movie
from .models import Tag


admin.site.site_header = 'KinoBase'

admin.site.register(Movie)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


admin.site.register(Tag, TagAdmin)

