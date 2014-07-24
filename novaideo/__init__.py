from pyramid.config import Configurator
from pyramid.i18n import TranslationStringFactory

from substanced.db import root_factory

_ =  TranslationStringFactory('novaideo')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.scan()
    return config.make_wsgi_app()
