# -*- coding: utf8 -*-
from zope.interface import Interface

from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service, get_oid

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles, has_role, get_current
from dace.interfaces import IEntity
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from pontus.schema import select, omit
from pontus.file import OBJECT_DATA

from ...user_management.behaviors import global_user_processsecurity
from novaideo.content.interface import IInvitation
from novaideo.content.person import Person
from novaideo.content.interface import IComment
from novaideo import _


def vote_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'subject')


def vote_roles_validation(process, context):
    return has_role(role=('Elector', process))

def vote_processsecurity_validation(process, context):
    user = get_current()
    return not (user in process.ballot.report.voters) and \
           global_user_processsecurity(process, context) 


class Vote(ElementaryAction):
    title = _('Vote')
    access_controled = True
    context = IEntity
    processs_relation_id = 'subject'
    relation_validation = vote_relation_validation
    roles_validation = vote_roles_validation
    processsecurity_validation = vote_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        vote_result = {}
        for v in appstruct['condidates']:
            vote_result[get_oid(v[OBJECT_DATA])] = v['judgment']

        user = get_current()
        ballot = self.process.ballot
        report = ballot.report
        votefactory = report.ballottype.vote_factory
        ballot.ballot_box.addtoproperty('votes', votefactory(vote_result))
        report.addtoproperty('voters', user)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@index'))



#TODO behaviors
