# -*- coding: utf8 -*-
# Copyright (c) 2015 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import pytz
import os
import logging
from persistent.list import PersistentList

from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationError
from pyramid.i18n import TranslationStringFactory
from pyramid.session import SignedCookieSessionFactory
from pyramid.threadlocal import get_current_request
from pyramid.i18n import default_locale_negotiator

from substanced.db import root_factory

from dace.util import getSite, find_service
from dace.objectofcollaboration.principal.util import grant_roles
from pontus.file import File

from novaideo.content.bot import Bot

#from zope.processlifetime import IDatabaseOpenedWithRoot
# from .twitter import start_ioloop


nothing = object()

log = logging.getLogger('novaideo')

_ = TranslationStringFactory('novaideo')


DEFAULT_SESSION_TIMEOUT = 25200


ANALYTICS_DEFAUT_CONTENTS = ['idea', 'proposal']


REPORTING_REASONS = {
    'sexual': {
        'order': 1,
        'title': _('Sexually explicit'),
        'description': _('The content is sexually explicit.')
    },
    'violent_dangerous': {
        'order': 2,
        'title': _('Violent or dangerous'),
        'description': _('The content is violent or dangerous.')
    },
    'hatred': {
        'order': 3,
        'title': _('Harrassment, intimidation or invitation to hate'),
        'description': _('The content harrasses, intimidates or invites to hate.')
    },
    'other': {
        'order': 100,
        'title': _('Other'),
        'description': _('Another reason? Please detail why you signal this content')
    }
}


VIEW_TYPES = {'default': _('Default view'),
              'bloc': _('Block view')}


ACCESS_ACTIONS = {}


def get_access_keys(context):
    declared = context.__provides__.declared
    if declared:
        for data in ACCESS_ACTIONS.get(declared[0], []):
            if data['access_key']:
                try:
                    return data['access_key'](context)
                except:
                    continue

    return ['always']


def get_novaideo_title():
    return getSite().title


def get_time_zone(request):
    #TODO get user timezone
    return pytz.timezone('Europe/Paris')


def ajax_api(request):
    return 'novaideoapi'


AVAILABLE_LANGUAGES = ['en', 'fr']


def my_locale_negotiator(request):
    locale = default_locale_negotiator(request)
    if locale is None and request.accept_language:
        locale = request.accept_language.best_match(AVAILABLE_LANGUAGES)

    return locale


def moderate_ideas(request):
    return getattr(request.root, 'moderate_ideas', False)


def moderate_proposals(request):
    return getattr(request.root, 'moderate_proposals', False)


def examine_ideas(request):
    return getattr(request.root, 'examine_ideas', False)


def examine_proposals(request):
    return getattr(request.root, 'examine_proposals', False)


def support_ideas(request):
    return getattr(request.root, 'support_ideas', False)


def support_proposals(request):
    return getattr(request.root, 'support_proposals', False)


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
        if hasattr(comment, 'formated_comment'):
            del comment.formated_comment

        if hasattr(comment, 'formated_urls'):
            del comment.formated_urls

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
    from BTrees.OOBTree import OOBTree

    contents = find_entities(
        interfaces=[IPerson]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        if hasattr(node, '_readed_at'):
            node._read_at = getattr(node, '_readed_at')
            del node._readed_at
        elif not hasattr(node, '_read_at'):
            node._read_at = OOBTree()

        log.info(str(index) + "/" + len_entities)

    log.info('Persons evolved.')


def evolve_access_keys(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IPerson
    from BTrees.OOBTree import OOBTree

    contents = find_entities(
        interfaces=[IPerson]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        node.reindex()
        log.info(str(index) + "/" + len_entities)

    log.info('Access keys evolved.')


def evolve_channel_comments_at(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IChannel
    from BTrees.OOBTree import OOBTree

    contents = find_entities(
        interfaces=[IChannel]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        node._comments_at = OOBTree()
        log.info(str(index) + "/" + len_entities)

    log.info('Channels evolved.')


def subscribe_users_newsletter(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IPerson

    if root.newsletters:
        contents = find_entities(
            interfaces=[IPerson]
            )
        newsletter = root.newsletters[0]
        len_entities = str(len(contents))
        for index, node in enumerate(contents):
            if getattr(node, 'email', '') and not newsletter.is_subscribed(node):
                newsletter.subscribe(
                    node.first_name, node.last_name, node.email)

            log.info(str(index) + "/" + len_entities)

        log.info('Channels evolved.')


def evolve_roles_comments(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IComment
    from dace.objectofcollaboration.principal.util import grant_roles
    contents = find_entities(interfaces=[IComment])
    for comment in contents:
        author = comment.author
        comment.edited = False
        comment.pinned = False
        grant_roles(user=author, roles=(('Owner', comment), ))
        comment.reindex()

    log.info('Comments evolved.')


def evolve_alerts(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IAlert
    from BTrees.OOBTree import OOBTree
    import transaction

    contents = find_entities(interfaces=[IAlert])
    len_entities = str(len(contents))
    for index, alert in enumerate(contents):
        alert.users_toexclude = OOBTree()
        alert.reindex()
        if index % 1000 == 0:
            log.info("**** Commit ****")
            transaction.commit()

        log.info(str(index) + "/" + len_entities)

    log.info('Alerts evolved')


def evolve_alert_subjects(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IAlert
    from novaideo.content.alert import InternalAlertKind
    from BTrees.OOBTree import OOBTree
    import transaction

    contents = find_entities(interfaces=[IAlert])
    len_entities = str(len(contents))
    for index, alert in enumerate(contents):
        if alert.kind == InternalAlertKind.comment_alert:
            if alert.subjects:
                subjects = alert.subjects
                subject = subjects[0] if subjects else root
                if hasattr(subject, 'channel'):
                    alert.delfromproperty('subjects', subject)
                    alert.addtoproperty('subjects', subject.channel)
                    alert.reindex()
                else:
                    root.delfromproperty('alerts', alert)

        if index % 1000 == 0:
            log.info("**** Commit ****")
            transaction.commit()

        log.info(str(index) + "/" + len_entities)

    log.info('Alerts evolved')


def subscribe_users_notif_ids(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IPerson

    contents = find_entities(
        interfaces=[IPerson]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        node.notification_ids = PersistentList([])
        log.info(str(index) + "/" + len_entities)

    log.info('Channels evolved.')


def evolve_mails(root, registry):
    from novaideo.mail import DEFAULT_SITE_MAILS
    result = []
    for mail in getattr(root, 'mail_templates', []):
        template = DEFAULT_SITE_MAILS.get(
            mail.get('mail_id', None), None)
        if template:
            mail['template'] = template['template']
            mail['subject'] = template['subject']

        result.append(mail)

    root.mail_templates = PersistentList(result)
    log.info('Emails evolved.')


def format_ideas(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import Iidea

    contents = find_entities(
        interfaces=[Iidea]
        )
    request = get_current_request()
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        if hasattr(node, 'formated_text'):
            del node.formated_text

        if hasattr(node, 'formated_urls'):
            del node.formated_urls

        node.format(request)
        log.info(str(index) + "/" + len_entities)

    log.info('Ideas evolved.')


def publish_comments(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IComment

    contents = find_entities(
        interfaces=[IComment]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        node.state = PersistentList(['published'])
        node.reindex()
        log.info(str(index) + "/" + len_entities)

    log.info('Comments published')


def evolve_nonproductive_cycle(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IProposal

    contents = find_entities(
        interfaces=[IProposal]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        working_group = node.working_group
        if working_group:
            working_group.init_nonproductive_cycle()

        log.info(str(index) + "/" + len_entities)

    log.info('Working group evolved')


def evolve_files(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IFile
    from novaideo.content.file import FileSchema, FileEntity
    from dace.objectofcollaboration.principal.util import (
        grant_roles, get_users_with_role)

    contents = find_entities(
        interfaces=[IFile]
        )
    len_entities = str(len(contents))
    schema = FileSchema()
    default_files = [f['name'] for f in DEFAULT_FILES]
    for index, node in enumerate(contents):
        data = node.get_data(schema)
        data.pop('_csrf_token_')
        new_file = FileEntity(**data)
        if not node.state:
            new_file.state = PersistentList(['draft'])
        else:
            new_file.state = node.state

        name = node.__name__
        new_file.__name__ = name
        users = get_users_with_role(('Owner', node))
        root.delfromproperty('files', node)
        root.addtoproperty('files', new_file)
        if users:
            author = users[0]
            grant_roles(user=author, roles=(('Owner', new_file), ))
            new_file.setproperty('author', author)
            new_file.reindex()

        if name in default_files:
            setattr(root, name, new_file)

        log.info(str(index) + "/" + len_entities)

    log.info('Files evolved')


def add_nia_bot(root):
    nia_picture = os.path.join(
        os.path.dirname(__file__), 'static', 'images', 'nia.png')
    picture = None
    if os.path.exists(nia_picture):
        buf = open(nia_picture, mode='rb')
        picture = File(
            fp=buf, filename='nia', mimetype='image/png')

    nia = root['principals']['users'].get('nia', None)
    if nia is None:
        nia = Bot(
            title='Nia',
            picture=picture
            )
        root['principals']['users']['nia'] = nia
        grant_roles(nia, ('Bot',), root=root)


def evolve_add_nia_bot(root, registry):
    root = getSite()
    add_nia_bot(root)


def add_guide_tour_data(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IPerson
    from persistent.dict import PersistentDict

    contents = find_entities(
        interfaces=[IPerson]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        if not hasattr(node, 'guide_tour_data'):
            node.guide_tour_data = PersistentDict({})

        log.info(str(index) + "/" + len_entities)

    log.info('Guide tour data evolved.')


def init_guide_tour_data(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IPerson
    from persistent.dict import PersistentDict

    contents = find_entities(
        interfaces=[IPerson]
        )
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        node.guide_tour_data = PersistentDict({})

        log.info(str(index) + "/" + len_entities)

    log.info('Guide tour data evolved.')


def evolve_related_correlation(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IComment, IAnswer

    contents = find_entities(
        interfaces=[IComment, IAnswer]
        )
    root = getSite()
    len_entities = str(len(contents))
    for index, node in enumerate(contents):
        if node.related_correlation:
            targets = node.related_correlation.targets
            if node in targets:
                targets.remove(node)

            node.set_associated_contents(
                targets, node.related_correlation.author)
            root.delfromproperty('correlations', node.related_correlation)

        node.reindex()
        log.info(str(index) + "/" + len_entities)

    log.info('Related correlations evolved')


def publish_organizations(root, registry):
    from novaideo.views.filter import find_entities
    from novaideo.content.interface import IOrganization

    contents = find_entities(interfaces=[IOrganization])
    for org in contents:
        org.state = PersistentList(['published'])
        org.reindex()

    log.info('Orgnaizations evolved.')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.add_request_method(ajax_api, reify=True)
    config.add_request_method(get_time_zone, reify=True)
    config.add_request_method(moderate_ideas, reify=True)
    config.add_request_method(moderate_proposals, reify=True)
    config.add_request_method(examine_ideas, reify=True)
    config.add_request_method(examine_proposals, reify=True)
    config.add_request_method(support_ideas, reify=True)
    config.add_request_method(support_proposals, reify=True)
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
    config.add_evolution_step(evolve_channel_comments_at)
    config.add_evolution_step(subscribe_users_newsletter)
    config.add_evolution_step(evolve_roles_comments)
    config.add_evolution_step(evolve_alerts)
    config.add_evolution_step(evolve_alert_subjects)
    config.add_evolution_step(subscribe_users_notif_ids)
    config.add_evolution_step(evolve_mails)
    config.add_evolution_step(evolve_access_keys)
    config.add_evolution_step(format_ideas)
    config.add_evolution_step(publish_comments)
    config.add_evolution_step(evolve_nonproductive_cycle)
    config.add_evolution_step(evolve_files)
    config.add_evolution_step(evolve_add_nia_bot)
    config.add_evolution_step(add_guide_tour_data)
    config.add_evolution_step(init_guide_tour_data)
    config.add_evolution_step(evolve_related_correlation)
    config.add_evolution_step(publish_organizations)
    config.add_translation_dirs('novaideo:locale/')
    config.add_translation_dirs('pontus:locale/')
    config.add_translation_dirs('dace:locale/')
    config.add_translation_dirs('deform:locale/')
    config.add_translation_dirs('colander:locale/')
    config.scan()
    config.add_static_view('novaideostatic',
                           'novaideo:static',
                           cache_max_age=86400)
    # config.add_subscriber(start_ioloop, IDatabaseOpenedWithRoot)
    config.set_locale_negotiator(my_locale_negotiator)
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
     'title': _('Legal notice'),
     'description': _('The legal notice'),
     'content': '',
     'content_file': 'legal_notices.html'},
    {'name': 'terms_of_use',
     'title': _('Terms of use'),
     'description': _('The terms of use'),
     'content': '',
     'content_file': 'terms_of_use.html'}
]
