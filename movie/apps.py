from django.apps import AppConfig


class MoviesConfig(AppConfig):
    name = 'movie'

    def ready(self):
        import movie.signals