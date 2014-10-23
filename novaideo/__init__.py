from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.i18n import TranslationStringFactory
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from substanced.db import root_factory


_ = TranslationStringFactory('novaideo')

default_session_timeout = 25200


def my_locale_negotiator(request):
    return request.accept_language.best_match(('en', 'fr'), 'fr')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.add_translation_dirs('novaideo:locale/')
    config.add_translation_dirs('deform:locale/')
    config.add_translation_dirs('colander:locale/')
    config.scan()
    YEAR = 86400 * 365
    config.add_static_view('novaideostatic', 'novaideo:static', cache_max_age=YEAR)
    #    config.set_locale_negotiator(my_locale_negotiator)
    settings = config.registry.settings
    secret = settings.get('novaideo.secret')
    if secret is None:
        raise ConfigurationError(
            'You must set a novaideo.secret key in your .ini file')
    session_factory = UnencryptedCookieSessionFactoryConfig(secret, timeout=default_session_timeout)#TODO 
    config.set_session_factory(session_factory)
    return config.make_wsgi_app()
