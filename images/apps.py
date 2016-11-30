from django.apps import AppConfig


class ImageConfig(AppConfig):
    name = 'images'
    verbose_name = 'Images bookmarks'

    def ready(self):
        import images.signals   # signal handler
