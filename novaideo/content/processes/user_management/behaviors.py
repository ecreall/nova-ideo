# -*- coding: utf8 -*-
import datetime
from pyramid.httpexceptions import HTTPFound
from substanced.util import find_service

from dace.util import getSite
from dace.objectofcollaboration.principal.util import grant_roles, has_any_roles, get_current, Anonymous
from dace.processinstance.activity import (
    ElementaryAction,
    LimitedCardinality,
    InfiniteCardinality,
    ActionType,
    StartStep,
    EndStep)

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import INovaIdeoApplication, IPerson
from novaideo.content.token import Token
from novaideo.mail import CONFIRMATION_MESSAGE
from novaideo import _
from novaideo.core import acces_action


def global_user_processsecurity(process, context):
    user = get_current()
    state = list(getattr(user, 'state', []))

    if has_any_roles(roles=('Admin',)) and not 'active' in state:
        state.append('active')

    return 'active' in state


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
        person.state.append('active')
        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        person.setproperty('keywords_ref', result)
        for i in range(root.tokens_mini):
            token = Token(title='Token_'+str(i))
            person.addtoproperty('tokens_ref', token)
            person.addtoproperty('tokens', token)
            token.setproperty('owner', person)

        message = CONFIRMATION_MESSAGE.format(person=person)
        mailer_send(subject='Confirmation de votre inscription',
                recipients=[person.email], body=message)

        person.reindex()
        return True

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def editsup_relation_validation(process, context):
    return True


def editsup_roles_validation(process, context):
    return has_any_roles(roles=('Admin',))


def editsup_processsecurity_validation(process, context):
    return True


def editsup_state_validation(process, context):
    return 'active' in context.state


class EditSuper(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
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
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    return 'active' in context.state


class Edit(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
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


def deactivate_relation_validation(process, context):
    return True


def deactivate_roles_validation(process, context):
    return has_any_roles(roles=('Admin',))


def deactivate_processsecurity_validation(process, context):
    return True


def deactivate_state_validation(process, context):
    return 'active' in context.state


class Deactivate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    title = _('Deactivate')
    context = IPerson
    relation_validation = deactivate_relation_validation
    roles_validation = deactivate_roles_validation
    processsecurity_validation = deactivate_processsecurity_validation
    state_validation = deactivate_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('active')
        context.state.append('deactivated')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def activate_relation_validation(process, context):
    return True


def activate_roles_validation(process, context):
    return has_any_roles(roles=('Admin',))


def activate_processsecurity_validation(process, context):
    return True


def activate_state_validation(process, context):
    return 'deactivated' in context.state


class Activate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    title = _('Activate')
    context = IPerson
    relation_validation = activate_relation_validation
    roles_validation = activate_roles_validation
    processsecurity_validation = activate_processsecurity_validation
    state_validation = activate_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('deactivated')
        context.state.append('active')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seeperson_processsecurity_validation(process, context):
    return 'active' in context.state


@acces_action()
class SeePerson(InfiniteCardinality):
    title = _('Details')
    context = IPerson
    actionType = ActionType.automatic
    processsecurity_validation = seeperson_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

#TODO behaviors
