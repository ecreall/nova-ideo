# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_role, get_current, has_any_roles)
from dace.interfaces import IEntity
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)
from dace.processinstance.core import PROCESS_HISTORY_KEY

from novaideo.content.interface import (
    INovaIdeoApplication,
    INode)
from novaideo.content.proposal import Proposal
from novaideo import _
from ..user_management.behaviors import (
    global_user_processsecurity, access_user_processsecurity)
from novaideo.core import access_action
from novaideo.utilities.alerts_utility import alert


def search_processsecurity_validation(process, context):
    return access_user_processsecurity(process, context)


@access_action()
class Search(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    actionType = ActionType.automatic
    processsecurity_validation = search_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        content_types = appstruct['content_types']
        text = appstruct['text_to_search']
        return {'content_types': content_types,
                'text': text}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(
            request.resource_url(
                root,
                query={'text_to_search': kw['text'],
                       'content_types': ",".join(kw['content_types'])}))


def home_processsecurity_validation(process, context):
    return True


@access_action()
class SeeHome(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    actionType = ActionType.automatic
    processsecurity_validation = home_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}


def seemy_roles_validation(process, context):
    return has_role(role=('Member',))


def seemyc_processsecurity_validation(process, context):
    user = get_current()
    contents = [o for o in getattr(user, 'contents', [])]
    return contents and global_user_processsecurity(process, context)


class SeeMyContents(InfiniteCardinality):
    style_picto = 'glyphicon glyphicon-inbox'
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemyc_processsecurity_validation

    def contents_nb(self, request, context):
        user = get_current()
        contents = [o for o in getattr(user, 'contents', [])]
        if getattr(request, 'is_idea_box', False):
            return len([s for s in contents
                        if not isinstance(s, Proposal)])

        return len(contents)

    def start(self, context, request, appstruct, **kw):
        return {}


def seemys_processsecurity_validation(process, context):
    user = get_current()
    selections = [o for o in getattr(user, 'selections', [])
                  if 'archived' not in o.state]
    return selections and global_user_processsecurity(process, context)


class SeeMySelections(InfiniteCardinality):
    style_picto = 'glyphicon glyphicon-star'
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemys_processsecurity_validation

    def contents_nb(self, request, context):
        user = get_current()
        selections = [o for o in getattr(user, 'selections', [])
                      if 'archived' not in o.state]
        if getattr(request, 'is_idea_box', False):
            return len([s for s in selections
                        if not isinstance(s, Proposal)])

        return len(selections)

    def start(self, context, request, appstruct, **kw):
        return {}


def seemypa_processsecurity_validation(process, context):
    user = get_current()
    if getattr(context, 'is_idea_box', False):
        return False

    return getattr(user, 'participations', []) and \
                   global_user_processsecurity(process, context)


class SeeMyParticipations(InfiniteCardinality):
    style_picto = 'novaideo-icon icon-wg'
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemypa_processsecurity_validation

    def contents_nb(self, request, context):
        user = get_current()
        return len(getattr(user, 'participations', []))

    def start(self, context, request, appstruct, **kw):
        return {}


def seemysu_processsecurity_validation(process, context):
    user = get_current()
    if getattr(context, 'is_idea_box', False):
        return False

    supports = [o for o in getattr(user, 'supports', [])
                if 'archived' not in o.state]
    return supports and global_user_processsecurity(process, context)


class SeeMySupports(InfiniteCardinality):
    style_picto = 'glyphicon glyphicon-hand-down'
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemysu_processsecurity_validation

    def contents_nb(self, request, context):
        user = get_current()
        len_supports = len([o for o in getattr(user, 'supports', [])
                            if 'archived' not in o.state])
        return str(len_supports)+'/'+str(len(getattr(user, 'tokens_ref', [])))

    def start(self, context, request, appstruct, **kw):
        return {}


def seeproposals_roles_validation(process, context):
    return has_role(role=('Examiner', ))


def seeproposals_processsecurity_validation(process, context):
    if getattr(context, 'is_idea_box', False):
        return False

    return 'proposal' in getattr(context, 'content_to_examine', [] ) and\
           global_user_processsecurity(process, context)


class SeeOrderedProposal(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'octicon octicon-checklist'
    style_order = -2
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeproposals_roles_validation
    processsecurity_validation = seeproposals_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def seeindeas_roles_validation(process, context):
    return has_role(role=('Examiner', ))


def seeindeas_processsecurity_validation(process, context):
    return 'idea' in getattr(context, 'content_to_examine', [] ) and\
           global_user_processsecurity(process, context)


class SeeIdeasToExamine(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'octicon octicon-checklist'
    style_order = -3
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeindeas_roles_validation
    processsecurity_validation = seeindeas_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def seeindeasm_roles_validation(process, context):
    return has_role(role=('Moderator', ))


def seeindeasm_processsecurity_validation(process, context):
    return getattr(context, 'moderate_ideas', False) and\
           global_user_processsecurity(process, context)


class SeeIdeasToModerate(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'octicon octicon-check'
    style_order = -4
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeindeasm_roles_validation
    processsecurity_validation = seeindeasm_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def history_roles_validation(process, context):
    return has_any_roles(roles=('PortalManager', ('Owner', context)))


def history_processsecurity_validation(process, context):
    return getattr(context, 'annotations', {}).get(PROCESS_HISTORY_KEY, {}) and \
           global_user_processsecurity(process, context)


class SeeEntityHistory(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-time'
    title = _('Processes history')
    style_order = 2
    isSequential = False
    context = IEntity
    processsecurity_validation = history_processsecurity_validation
    roles_validation = history_roles_validation

    def start(self, context, request, appstruct, **kw):
        return {}


def contact_processsecurity_validation(process, context):
    root = getSite()
    for contact in getattr(root, 'contacts', []):
        if contact.get('email', None):
            return True

    return False


class Contact(InfiniteCardinality):
    style = 'button'
    style_descriminator = 'footer-action'
    style_interaction = 'modal-action'
    style_picto = 'glyphicon glyphicon-send'
    submission_title = _('Send')
    style_order = 1
    isSequential = False
    context = IEntity
    processsecurity_validation = contact_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        subject = appstruct.get('subject')
        mail = appstruct.get('message')
        sender = appstruct.get('email')
        services = appstruct.get('services')
        alert('email', [sender], list(services),
              subject=subject, body=mail)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(
            request.resource_url(context, ''))


def seealerts_roles_validation(process, context):
    return has_role(role=('Member',))


def seealerts_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeAlerts(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    processsecurity_validation = seealerts_processsecurity_validation
    roles_validation = seealerts_roles_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        for alert in user.alerts:
            alert.unsubscribe(user)

        return {}


def seeusers_roles_validation(process, context):
    return has_role(role=('Member', ))


def seeusers_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeUsers(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-user'
    style_order = 0
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeusers_roles_validation
    processsecurity_validation = seeusers_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def seeanalytics_roles_validation(process, context):
    return has_role(role=('Examiner', ))


def seeanalytics_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class SeeAnalytics(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-equalizer'
    style_order = -1
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seeanalytics_roles_validation
    processsecurity_validation = seeanalytics_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


def seegraph_roles_validation(process, context):
    return has_role(role=('Member',))


def seegraph_processsecurity_validation(process, context):
    graph = getattr(context, 'graph', {})
    return len(graph) > 1 and \
        global_user_processsecurity(process, context)


class SeeGraph(InfiniteCardinality):
    style_descriminator = 'plus-action'
    style_interaction = 'modal-action'
    style_modal = 'modal-xl'
    style_picto = 'ion-android-share'
    style_order = 1
    isSequential = False
    context = INode
    processsecurity_validation = seegraph_processsecurity_validation
    roles_validation = seegraph_roles_validation

    def start(self, context, request, appstruct, **kw):
        return {}

#TODO behaviors
