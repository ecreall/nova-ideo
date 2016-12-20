# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.httpexceptions import HTTPFound

from dace.objectofcollaboration.principal.util import get_current
from dace.interfaces import IEntity
from dace.processinstance.activity import InfiniteCardinality

from ..user_management.behaviors import global_user_processsecurity
from novaideo import _


def vote_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'subject')


def vote_processsecurity_validation(process, context):
    user = get_current()
    report = process.ballot.report
    return user in report.electors and \
           user not in report.voters and \
           global_user_processsecurity()


class VoteBase(InfiniteCardinality):
    title = _('Vote')
    submission_title = _('Save')
    access_controled = True
    context = IEntity
    processs_relation_id = 'subject'
    relation_validation = vote_relation_validation
    processsecurity_validation = vote_processsecurity_validation

    def after_execution(self, context, request, **kw):
        if self.isSequential:
            self.unlock(request)
            self.workitem.unlock(request)

        report = self.process.ballot.report
        if len(report.electors) == len(report.voters):
            self.isexecuted = True
            self.workitem.node.finish_behavior(self.workitem)

    def close_vote(self, context, request, **kw):
        self.workitem.node.finish_behavior(self.workitem)

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@index'))


def remove_vote_processes(ballot_action, runtime):
    ballot_process = ballot_action.sub_process
    if ballot_process:
        runtime.delfromproperty('processes', ballot_process)
        exec_ctx = ballot_process.execution_context
        vote_processes = exec_ctx.get_involved_collection(
            'vote_processes')
        for v_proc in vote_processes:
            runtime.delfromproperty('processes', v_proc)


def remove_elector_vote_processes(ballot_action, user):
    ballot_process = ballot_action.sub_process
    ballots = ballot_process.ballots
    for ballot in ballots:
        report = ballot.report
        if user in report.electors and user not in report.voters:
            report.delfromproperty('electors', user)
