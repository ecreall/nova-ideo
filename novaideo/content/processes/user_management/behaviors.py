# -*- coding: utf8 -*-
import datetime
from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service, get_oid

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles, has_any_roles
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)
from pontus.schema import select, omit

from novaideo.ips.xlreader import creat_object_from_xl
from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import INovaIdeoApplication, IPerson
from novaideo.content.person import Person
from novaideo import _


confiramtion_message = u"""
Bonjour {person.user_title} {person.last_name} {person.first_name},

Confiramtion de votre inscription.

Cordialement,

La Plateforme NovaIdeo
"""


def reg_relation_validation(process, context):
    return True


def reg_roles_validation(process, context):
    return has_any_roles(roles=('Anonymous',))


def reg_processsecurity_validation(process, context):
    return True


def reg_state_validation(process, context):
    return True


class Registration(InfiniteCardinality):
    context = INovaIdeoApplication
    relation_validation = reg_relation_validation
    roles_validation = reg_roles_validation
    processsecurity_validation = reg_processsecurity_validation
    state_validation = reg_state_validation

    def start(self, context, request, appstruct, **kw):
        person = appstruct['_object_data']
        root = getSite(context)
        principals = find_service(root, 'principals')
        name = person.first_name + ' ' +person.last_name
        principals['users'][name] = person
        grant_roles(person, roles=('Member',))
        grant_roles(person, (('Owner', person),))
        person.state.append('created')
        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        person.setproperty('keywords_ref', result)
        message = confiramtion_message.format(person=person)
        mailer_send(subject='Confiramtion', recipients=[person.email], body=message )
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root, "@@index"))


def editsup_relation_validation(process, context):
    return True


def editsup_roles_validation(process, context):
    return has_any_roles(roles=('Admin',)) 


def editsup_processsecurity_validation(process, context):
    return True


def editsup_state_validation(process, context):
    return 'created' in context.state


class EditSuper(InfiniteCardinality):
    title = _('Edit')
    context = IPerson
    relation_validation = editsup_relation_validation
    roles_validation = editsup_roles_validation
    processsecurity_validation = editsup_processsecurity_validation
    state_validation = editsup_state_validation

    def start(self, context, request, appstruct, **kw):
        context.modified_at = datetime.datetime.today()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def edit_relation_validation(process, context):
    return True


def edit_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),)) 


def edit_processsecurity_validation(process, context):
    return True


def edit_state_validation(process, context):
    return 'created' in context.state


class Edit(InfiniteCardinality):
    title = _('Edit')
    context = IPerson
    relation_validation = edit_relation_validation
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        context.setproperty('keywords_ref', result)
        context.modified_at = datetime.datetime.today()
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))
#TODO bihaviors
