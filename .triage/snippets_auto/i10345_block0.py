"""
ASGI config for any ft_core based project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import multiprocessing
import os

from django import setup
from django.core.asgi import get_asgi_application as django_asgi_application

from .protocol_router import Router


def get_asgi_application():
    # from ft_core.multiprocessing.functions import on_exit_hook, on_starting_hook
    from ft_core.settings.functions import get_env

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    setup(set_prefix=False)
    django_application = django_asgi_application()

    from django.conf import settings

    force_forkserver = get_env("FORCE_FORKSERVER", default=False, as_bool=True)
    if os.name != "nt" and (not settings.DEBUG or force_forkserver):
        multiprocessing.set_start_method("forkserver")

    if settings.DEBUG and not force_forkserver:
        # on_starting_hook(None)
        # atexit.register(lambda: on_exit_hook(None))
        pass

    from ft_core.graphql.schema import get_schema

    return Router(
        schema=get_schema(),
        django_application=django_application,
        graphql_ide="graphiql" if settings.DEBUG else None,
        multipart_uploads_enabled=False,
    )

