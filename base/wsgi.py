import os

from django.core.wsgi import get_wsgi_application

from .settings import DjangoUtil; DjangoUtil.init()

application = get_wsgi_application()
