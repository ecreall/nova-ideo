# -*- coding: utf8 -*-
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import has_role, get_current
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)

from novaideo.content.interface import INovaIdeoApplication, IProposal
from novaideo import _
from ..user_management.behaviors import global_user_processsecurity
from novaideo.core import acces_action


@acces_action()
class Search(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    actionType = ActionType.automatic

    def start(self, context, request, appstruct, **kw):
        self.content_types = appstruct['content_types']
        self.text = appstruct['text']
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(
                  request.resource_url(root, 
                        query={'text': self.text,
                               'content_types': ",".join(self.content_types)}))


def seemy_roles_validation(process, context):
    return has_role(role=('Member',))


def seemyc_processsecurity_validation(process, context):
    user = get_current()
    contents = [o for o in getattr(user, 'contents', []) \
                if not('archived' in o.state)]
    return contents and global_user_processsecurity(process, context)

class SeeMyContents(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemyc_processsecurity_validation

    def contents_nb(self):
        user = get_current()
        return len([o for o in getattr(user, 'contents', []) \
                    if not('archived' in o.state)])

    def start(self, context, request, appstruct, **kw):
        return True

def seemys_processsecurity_validation(process, context):
    user = get_current()
    selections = [o for o in getattr(user, 'selections', []) \
                  if not('archived' in o.state)]
    return selections and global_user_processsecurity(process, context)


class SeeMySelections(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemys_processsecurity_validation

    def contents_nb(self):
        user = get_current()
        return len([o for o in getattr(user, 'selections', []) \
                    if not('archived' in o.state)])

    def start(self, context, request, appstruct, **kw):
        return True


def seemypa_processsecurity_validation(process, context):
    user = get_current()
    return getattr(user, 'participations', []) and \
                   global_user_processsecurity(process, context)


class SeeMyParticipations(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemypa_processsecurity_validation


    def contents_nb(self):
        user = get_current()
        return len(getattr(user, 'participations', []))

    def start(self, context, request, appstruct, **kw):
        return True


def seemysu_processsecurity_validation(process, context):
    user = get_current()
    supports = [o for o in getattr(user, 'supports', []) \
                if not('archived' in o.state)]
    return supports and global_user_processsecurity(process, context)


class SeeMySupports(InfiniteCardinality):
    isSequential = False
    context = INovaIdeoApplication
    roles_validation = seemy_roles_validation
    processsecurity_validation = seemysu_processsecurity_validation

    def contents_nb(self):
        user = get_current()
        return len([o for o in getattr(user, 'supports', []) \
                    if not('archived' in o.state)])

    def start(self, context, request, appstruct, **kw):
        return True


def seeproposal_processsecurity_validation(process, context):
    return not ('draft' in context.state) or \
           has_role(role=('Owner', context))
           

@acces_action()
class SeeProposal(InfiniteCardinality):
    title = _('Details')
    context = IProposal
    actionType = ActionType.automatic
    processsecurity_validation = seeproposal_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
