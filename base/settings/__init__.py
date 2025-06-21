import os
from importlib import import_module
from decouple import config
class Util:
    NAME = ''

    @classmethod
    def settings_path(cls):
        os.environ['SITE'] = 'nimbus'
        return 'sites.%s.settings.%s' % (os.environ['SITE'], cls.NAME)

    @classmethod
    def settings(cls):
        return import_module(cls.settings_path())

    @classmethod
    def import_to(cls, module, var_dict):
        try:
            names = module.__all__
        except AttributeError:
            names = [name for name in module.__dict__ if not name.startswith('_')]
        var_dict.update({name: getattr(module, name) for name in names})

class DjangoUtil(Util):
    NAME = 'django'

    @classmethod
    def init(cls):
        os.environ['DJANGO_SETTINGS_MODULE'] = cls.settings_path()

    @classmethod
    def setup(cls):
        cls.init()

        from django import setup
        setup()

    @classmethod
    def init_sites(cls):
        from django.contrib.sites.models import Site

        for domain in config('SITE').split(' '):
            try:
                site = Site.objects.get(domain=domain)
            except Site.DoesNotExist:
                site = Site.objects.create(domain=domain, name=domain.split('.')[0].capitalize())

    @classmethod
    def init_admin(cls):
        from django.contrib.auth import get_user_model

        username, email, password = [os.environ[x] for x in ('ENV_ADMIN_USERNAME', 'ENV_ADMIN_EMAIL', 'ENV_ADMIN_PASSWORD')]
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
            user.email = email
            user.set_password(password)
            user.save()
        except user_model.DoesNotExist:
            user_model.objects.create_superuser(username, email, password)

    @classmethod
    def get_absolute_url(cls, request, path):
        from urllib.parse import urlunsplit
        return urlunsplit([request.scheme, request.get_host(), path, '', ''])
