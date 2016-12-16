# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry

from substanced.util import get_oid

from dace.objectofcollaboration.principal.util import (
    has_role,
    grant_roles,
    get_current,
    get_users_with_role)
from dace.processinstance.activity import InfiniteCardinality
from dace.util import find_catalog

from ..user_management.behaviors import global_user_processsecurity
from novaideo.content.interface import (
    ISignalableEntity,
    ISReport)
from novaideo import _, nothing
from novaideo.views.filter import find_entities
from novaideo.adapters.report_adapter import ISignalableObject
from novaideo.utilities.alerts_utility import alert
from novaideo.content.alert import InternalAlertKind


def select_roles_validation(process, context):
    return has_role(role=('Member',))


def select_processsecurity_validation(process, context):
    return global_user_processsecurity()


def select_state_validation(process, context):
    return "published" in context.state


class Report(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'md md-sms-failed'
    style_order = 100
    isSequential = False
    submission_title = _('Continue')
    context = ISignalableEntity
    roles_validation = select_roles_validation
    processsecurity_validation = select_processsecurity_validation
    state_validation = select_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        report = appstruct['_object_data']
        context.addtoproperty('reports', report)
        report.state.append('pending')
        context.state.append('reported')
        grant_roles(user=user, roles=(('Owner', report), ))
        report.setproperty('author', user)
        report.reindex()
        context.reindex()
        moderators = get_users_with_role(role='Moderator')
        alert(
            'internal', [request.root], moderators,
            internal_kind=InternalAlertKind.moderation_alert,
            subjects=[context], alert_kind='new_report')
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def decision_roles_validation(process, context):
    return has_role(role=('Moderator',))


def decision_processsecurity_validation(process, context):
    return global_user_processsecurity()


def decision_state_validation(process, context):
    return "reported" in context.state


class Ignore(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-play-circle'
    style_order = 100
    isSequential = False
    submission_title = _('Continue')
    context = ISignalableEntity
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        context_oid = get_oid(context)
        dace_index = find_catalog('dace')
        dace_container_oid = dace_index['container_oid']
        query = dace_container_oid.eq(context_oid)
        reports = find_entities(
            interfaces=[ISReport],
            metadata_filter={
                'states': ['pending']},
            user=user,
            add_query=query)
        for report in reports:
            report.state = PersistentList(['processed'])
            report.reindex()

        context.init_len_current_reports()
        context.state.remove('reported')
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


class Censor(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-eye-close'
    style_order = 101
    isSequential = False
    submission_title = _('Continue')
    context = ISignalableEntity
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        report = appstruct['_object_data']
        context.addtoproperty('censoring_reason', report)
        grant_roles(user=user, roles=(('Owner', report), ))
        report.setproperty('author', user)
        report.reindex()
        context_oid = get_oid(context)
        dace_index = find_catalog('dace')
        dace_container_oid = dace_index['container_oid']
        query = dace_container_oid.eq(context_oid)
        reports = find_entities(
            interfaces=[ISReport],
            metadata_filter={
                'states': ['pending']},
            add_query=query)
        for report in reports:
            report.state = PersistentList(['processed'])
            report.reindex()

        context.init_len_current_reports()
        adapter = get_current_registry().queryAdapter(
            context, ISignalableObject)
        if adapter is not None:
            context.state.remove('reported')
            adapter.censor(request)

        return {}

    def redirect(self, context, request, **kw):
        return nothing


def restor_state_validation(process, context):
    return "censored" in context.state


class Restor(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-refresh'
    style_order = 102
    isSequential = False
    submission_title = _('Continue')
    context = ISignalableEntity
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = restor_state_validation

    def start(self, context, request, appstruct, **kw):
        adapter = get_current_registry().queryAdapter(
            context, ISignalableObject)
        if adapter is not None:
            adapter.restor(request)

        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def seerep_processsecurity_validation(process, context):
    return getattr(context, 'len_reports', 0) and global_user_processsecurity()


class SeeReports(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'communication-action'
    style_picto = 'md md-sms-failed'
    style_interaction = 'ajax-action'
    style_interaction_type = 'sidebar'
    style_order = 103
    context = ISignalableEntity
    roles_validation = decision_roles_validation
    processsecurity_validation = seerep_processsecurity_validation

    def get_nb(self, context, request):
        return getattr(context, 'len_current_reports', 0)

    def get_title(self, context, request, nb_only=False):
        len_reports = self.get_nb(context, request)
        if nb_only:
            return str(len_reports)

        return _("${title} (${nember})",
                 mapping={'nember': len_reports,
                          'title': request.localizer.translate(self.title)})

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return nothing


#TODO behaviors
