# -*- coding: utf8 -*-
from pyramid.httpexceptions import HTTPFound

from dace.objectofcollaboration.principal.util import has_role, get_current
from dace.interfaces import IEntity
from dace.processinstance.activity import (
    ElementaryAction)

from ...user_management.behaviors import global_user_processsecurity
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
        vote = appstruct['vote']
        user = get_current()
        ballot = self.process.ballot
        report = ballot.report
        votefactory = report.ballottype.vote_factory
        ballot.ballot_box.addtoproperty('votes', votefactory(vote))
        report.addtoproperty('voters', user)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@index'))


#TODO behaviors