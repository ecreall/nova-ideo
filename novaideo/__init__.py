# -*- coding: utf8 -*-
# Copyright (c) 2015 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import logging
from persistent.list import PersistentList

from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.i18n import TranslationStringFactory
from pyramid.session import SignedCookieSessionFactory
from pyramid.threadlocal import get_current_request

from substanced.db import root_factory

from dace.util import getSite, find_service


log = logging.getLogger('novaideo')

_ = TranslationStringFactory('novaideo')


DEFAULT_SESSION_TIMEOUT = 25200


ANALYTICS_DEFAUT_CONTENTS = ['idea', 'proposal']


ACCESS_ACTIONS = {}


def get_access_keys(context):
    declared = context.__provides__.declared
    if declared:
        for data in ACCESS_ACTIONS.get(declared[0], []):
            if data['access_key']:
                return data['access_key'](context)

    return ['always']


def get_novaideo_title():
    return getSite().title


def my_locale_negotiator(request):
    return request.accept_language.best_match(('en', 'fr'), 'fr')


def moderate_ideas(request):
    return getattr(request.root, 'moderate_ideas', False)


def is_idea_box(request):
    return getattr(request.root, 'is_idea_box', False)


def content_to_examine(request):
    return getattr(request.root, 'content_to_examine', [])


def content_to_support(request):
    return getattr(request.root, 'content_to_support', [])


def accessible_to_anonymous(request):
    only_for_members = getattr(request.root, 'only_for_members', False)
    if not only_for_members or \
       (only_for_members and \
        request.user):
        return True

    return False


def analytics_default_content_types(request):
    if request.is_idea_box:
        return ['idea']
    else:
        return list(ANALYTICS_DEFAUT_CONTENTS)


def searchable_contents(request):
    from novaideo.core import SEARCHABLE_CONTENTS
    searchable_contents = dict(SEARCHABLE_CONTENTS)
    modes = request.root.get_work_modes()
    # searchable_contents.pop('webadvertising')
    # searchable_contents.pop('file')
    if 'amendment' not in modes:
        searchable_contents.pop('amendment')

    if getattr(request, 'is_idea_box', False):
        searchable_contents.pop('proposal')
        return searchable_contents

    return searchable_contents


def evolve_wg(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IWorkingGroup
    import transaction

    contents = find_entities(interfaces=[IWorkingGroup])
    len_entities = str(len(contents))
    for index, wg in enumerate(contents):
        if hasattr(wg, 'first_decision'):
            wg.first_improvement_cycle = wg.first_decision
            wg.reindex()

        if index % 1000 == 0:
            log.info("**** Commit ****")
            transaction.commit()

        log.info(str(index) + "/" + len_entities)

    log.info('Working groups evolved.')


def update_len_comments(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import ICommentable
    import transaction

    contents = find_entities(interfaces=[ICommentable])
    len_entities = str(len(contents))
    for index, content in enumerate(contents):
        content.update_len_comments()
        if index % 1000 == 0:
            log.info("**** Commit ****")
            transaction.commit()

        log.info(str(index) + "/" + len_entities)

    log.info('Len comments updated')


def update_len_selections(root, registry):
    from novaideo.views.filter import find_entities, get_users_by_preferences
    from novaideo.content.interface import ISearchableEntity
    import transaction

    contents = find_entities(interfaces=[ISearchableEntity])
    len_entities = str(len(contents))
    for index, content in enumerate(contents):
        result = get_users_by_preferences(content)
        content.len_selections = len(result)
        if index % 1000 == 0:
            log.info("**** Commit ****")
            transaction.commit()

        log.info(str(index) + "/" + len_entities)

    log.info('Len comments updated')


def evolve_states_ideas(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import Iidea
    from persistent.list import PersistentList

    contents = find_entities(interfaces=[Iidea],
                             metadata_filter={'states': ['published']})
    len_entities = str(len(contents))
    idea_to_support = 'idea' in getattr(root, 'content_to_support', [])
    sates = ['published', 'submitted_support']
    if idea_to_support:
        sates = ['submitted_support', 'published']

    for index, idea in enumerate(contents):
        if 'examined' not in idea.state:
            idea.state = PersistentList(sates)
            idea.reindex()

        log.info(str(index) + "/" + len_entities)

    log.info('Ideas states evolved.')


def evolve_state_files(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IFile

    contents = find_entities(interfaces=[IFile])
    for file_ in contents:
        if not file_.state:
            file_.state = PersistentList(['draft'])
            file_.reindex()

    log.info('Working groups evolved.')


def evolve_process_def(root, registry):
    def_container = find_service('process_definition_container')
    for pd in def_container.definitions:
        pd.contexts = PersistentList([])

    log.info('Process def evolved.')


def evolve_comments(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IComment
    request = get_current_request()
    contents = find_entities(interfaces=[IComment])
    for comment in contents:
        comment.format(request)

    log.info('Comments evolved.')


def evolve_nodes(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import INode

    contents = find_entities(
        interfaces=[INode],
        include_archived=True,
        )
    len_entities = str(len(contents))
    newcalculated = []
    for index, node in enumerate(contents):
        oid = str(node.__oid__).replace('-', '_')
        if oid not in newcalculated:
            graph, newcalculated = node.init_graph(
                newcalculated)

        log.info(str(index) + "/" + len_entities)

    log.info('Nodes evolved.')


def evolve_channels(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import (
        Iidea, IAmendment, IProposal, ICorrelation,
        IPerson)
    from novaideo.core import Channel
    root = getSite()
    general = root.channels[0] if root.channels else Channel(title=_("General"))
    root.addtoproperty('channels', general)
    root.setproperty('general_chanel', general)
    contents = find_entities(
        interfaces=[Iidea, IAmendment, IProposal, ICorrelation])
    for entity in contents:
        if not entity.channel:
            entity.addtoproperty('channels', Channel())
            channel = entity.channel
            for comment in entity.comments:
                channel.addtoproperty('comments', comment)

    users = find_entities(
        interfaces=[IPerson])
    for member in users:
        selections = getattr(member, 'selections', [])
        for selection in selections:
            channel = getattr(selection, 'channel', None)
            if channel and member not in channel.members:
                channel.addtoproperty('members', member)

    log.info('Comments evolved.')


def evolve_person(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IPerson

    contents = find_entities(
        interfaces=[IPerson]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        node.reindex()
        log.info(str(index) + "/" + len_entities)

    log.info('Persons evolved.')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.add_request_method(moderate_ideas, reify=True)
    config.add_request_method(content_to_examine, reify=True)
    config.add_request_method(content_to_support, reify=True)
    config.add_request_method(is_idea_box, reify=True)
    config.add_request_method(accessible_to_anonymous, reify=True)
    config.add_request_method(searchable_contents, reify=True)
    config.add_request_method(analytics_default_content_types, reify=True)
    config.add_evolution_step(evolve_wg)
    config.add_evolution_step(evolve_states_ideas)
    config.add_evolution_step(evolve_state_files)
    config.add_evolution_step(update_len_comments)
    config.add_evolution_step(update_len_selections)
    config.add_evolution_step(evolve_process_def)
    config.add_evolution_step(evolve_comments)
    config.add_evolution_step(evolve_nodes)
    config.add_evolution_step(evolve_channels)
    config.add_evolution_step(evolve_person)
    config.add_translation_dirs('novaideo:locale/')
    config.add_translation_dirs('pontus:locale/')
    config.add_translation_dirs('dace:locale/')
    config.add_translation_dirs('deform:locale/')
    config.add_translation_dirs('colander:locale/')
    config.scan()
    config.add_static_view('novaideostatic',
                           'novaideo:static',
                           cache_max_age=86400)
    #    config.set_locale_negotiator(my_locale_negotiator)
    settings = config.registry.settings
    secret = settings.get('novaideo.secret')
    if secret is None:
        raise ConfigurationError(
            'You must set a novaideo.secret key in your .ini file')

    session_factory = SignedCookieSessionFactory(
        secret,
        timeout=DEFAULT_SESSION_TIMEOUT,
        reissue_time=3600)
    config.set_session_factory(session_factory)
    return config.make_wsgi_app()


DEFAULT_FILES = [
    {'name': 'ml_file',
     'title': _('Legal notices'),
     'description': _('The legal notices'),
     'content': ''},
    {'name': 'terms_of_use',
     'title': _('Terms of use'),
     'description': _('The terms of use'),
     'content': ''}
]
