# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from io import StringIO, BytesIO
import csv
import colander
import transaction
import uuid
import datetime
import pytz
import itertools
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.threadlocal import get_current_request
from pyramid import renderers
from pyramid.response import FileIter

from substanced.util import get_oid
from substanced.event import LoggedIn
from substanced.util import find_service

from dace.util import (
    getSite, name_chooser, name_normalizer,
    push_callback_after_commit, get_socket)
from dace.objectofcollaboration.principal.role import DACE_ROLES
from dace.objectofcollaboration.principal.util import (
    grant_roles,
    has_role,
    get_current,
    has_any_roles,
    revoke_roles,
    get_roles,
    get_users_with_role)
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)
from dace.processinstance.core import ActivityExecuted, PROCESS_HISTORY_KEY

from ..comment_management import VALIDATOR_BY_CONTEXT
from novaideo.content.interface import (
    INovaIdeoApplication, IPerson, IPreregistration)
from novaideo.content.person import (
    Person, PersonSchema, DEADLINE_PREREGISTRATION)
from novaideo.utilities.util import (
    to_localized_time, gen_random_token, connect)
from novaideo import _, nothing, my_locale_negotiator
from novaideo.core import (
    access_action, serialize_roles, PrivateChannel)
from novaideo.views.filter import get_users_by_preferences
from novaideo.content.alert import InternalAlertKind
from novaideo.utilities.alerts_utility import (
    alert, get_user_data, get_entity_data)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo.content.processes import (
    global_user_processsecurity, access_user_processsecurity)
from novaideo.role import get_authorized_roles
from novaideo.adapters import EXTRACTION_ATTR


def accept_preregistration(request, preregistration, root):
    preregistration.init_deadline(datetime.datetime.now(tz=pytz.UTC))
    if getattr(preregistration, 'email', ''):
        deadline_date = preregistration.get_deadline_date()
        locale = my_locale_negotiator(request)
        # url = request.resource_url(preregistration, "")
        url = request.route_url('registrations', preregistration.__name__)
        mail_template = root.get_mail_template(
            'preregistration', getattr(preregistration, 'locale', locale))
        email_data = get_user_data(preregistration, 'recipient', request)
        subject = mail_template['subject'].format(
            novaideo_title=root.title)
        deadline_str = to_localized_time(
            deadline_date, request, translate=True)
        message = mail_template['template'].format(
            url=url,
            deadline_date=deadline_str.lower(),
            novaideo_title=root.title,
            **email_data
            )
        alert('email', [root.get_site_sender()], [preregistration.email],
              subject=subject, body=message)


def login_roles_validation(process, context):
    return has_role(role=('Anonymous', ))


class LogIn(InfiniteCardinality):
    tags = ['main-menu', 'instance']
    title = _('Log in')
    access_controled = True
    context = INovaIdeoApplication
    roles_validation = login_roles_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def logout_roles_validation(process, context):
    return has_role(role=('Collaborator',))


class LogOut(InfiniteCardinality):
    tags = ['main-menu', 'instance']
    title = _('Log out')
    access_controled = True
    context = INovaIdeoApplication
    roles_validation = logout_roles_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def edit_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context), 'SiteAdmin'))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity()


def edit_state_validation(process, context):
    return 'active' in context.state


class Edit(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-settings'
    style_order = 1
    tags = ['primary', 'menu', 'main-menu']
    title = _('Edit')
    submission_title = _('Save')
    context = IPerson
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        organization = appstruct.get('organization', None)
        root = getSite()
        root.merge_keywords(context.keywords)
        context.set_title()
        context.set_organization(organization)
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        request.registry.notify(ActivityExecuted(self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class EditPassword(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-settings'
    style_order = 1
    tags = ['primary', 'menu', 'main-menu']
    title = _('Edit password')
    submission_title = _('Save')
    context = IPerson
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        current_user_password = appstruct['current_password']
        user = get_current()
        user_password = getattr(user, 'password', None)
        if not user_password or user.check_password(current_user_password):
            password = appstruct['password']
            context.set_password(password)
            context.reindex()

        request.registry.notify(ActivityExecuted(self, [context], user))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class GetAPIToken(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_picto = 'glyphicon glyphicon-wrench'
    style_order = 1
    tags = ['secondary', 'entity']
    title = _('Get API token')
    submission_title = _('Get a new API token')
    context = IPerson
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        password = appstruct['password']
        if context.check_password(password):
            context.api_token = uuid.uuid4().hex
            context.reindex()
            return {
                'api_token': context.api_token
            }

        return {}

    def redirect(self, context, request, **kw):
        query = {}
        if 'api_token' not in kw:
            query['invalid_password'] = True

        return HTTPFound(request.resource_url(
            context, "@@get_api_token", query=query))


def deactivate_roles_validation(process, context):
    return (context.organization and \
            has_role(role=('OrganizationResponsible',
                           context.organization))) or \
            has_role(role=('SiteAdmin',))


def deactivate_processsecurity_validation(process, context):
    return global_user_processsecurity()


def deactivate_state_validation(process, context):
    return 'active' in context.state


class Deactivate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_picto = 'glyphicon glyphicon-ban-circle'
    style_interaction = 'ajax-action'
    style_order = 0
    tags = ['secondary', 'entity']
    title = _('Disactivate the profile')
    submission_title = _('Continue')
    context = IPerson
    roles_validation = deactivate_roles_validation
    processsecurity_validation = deactivate_processsecurity_validation
    state_validation = deactivate_state_validation

    def start(self, context, request, appstruct, **kw):
        from ..proposal_management.behaviors import exclude_participant_from_wg
        root = getSite()
        context.state.remove('active')
        context.state.append('deactivated')
        context.set_organization(None)
        proposals = getattr(context, 'participations', [])
        anonymous_proposals = getattr(context.mask, 'participations', [])
        for proposal in proposals:
            exclude_participant_from_wg(
                proposal, request, context, root)

        for proposal in anonymous_proposals:
            exclude_participant_from_wg(
                proposal, request, context.mask, root)

        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        pref_author = list(get_users_by_preferences(context))
        alert('internal', [request.root], pref_author,
              internal_kind=InternalAlertKind.content_alert,
              subjects=[context], alert_kind='user_deactivated')
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def activate_roles_validation(process, context):
    return (context.organization and \
            has_role(role=('OrganizationResponsible',
                           context.organization))) or \
            has_role(role=('SiteAdmin',))


def activate_processsecurity_validation(process, context):
    return global_user_processsecurity()


def activate_state_validation(process, context):
    return 'deactivated' in context.state


class Activate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_picto = 'glyphicon glyphicon-ok-circle'
    style_order = 0
    tags = ['secondary', 'entity']
    title = _('Activate the profile')
    context = IPerson
    roles_validation = activate_roles_validation
    processsecurity_validation = activate_processsecurity_validation
    state_validation = activate_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('deactivated')
        context.state.append('active')
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reindex()
        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def assignroles_roles_validation(process, context):
    return has_role(role=('SiteAdmin', ))


def assignroles_processsecurity_validation(process, context):
    return global_user_processsecurity()


def assignroles_state_validation(process, context):
    return 'active' in context.state


class AssignRoles(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-tower'
    style_order = 2
    tags = ['secondary', 'entity']
    title = _('Assign roles')
    submission_title = _('Save')
    context = IPerson
    roles_validation = assignroles_roles_validation
    processsecurity_validation = assignroles_processsecurity_validation
    state_validation = assignroles_state_validation

    def start(self, context, request, appstruct, **kw):
        new_roles = list(appstruct['roles'])
        authorized_roles = get_authorized_roles()
        new_roles = [r for r in new_roles if r in authorized_roles]
        if new_roles:
            current_roles = [r for r in get_roles(context) if
                             not getattr(
                                 DACE_ROLES.get(r, None), 'islocal', False)]
            roles_to_revoke = [r for r in current_roles
                               if r not in new_roles]
            roles_to_grant = [r for r in new_roles
                              if r not in current_roles]
            revoke_roles(context, roles_to_revoke)
            grant_roles(context, roles_to_grant)
            context.modified_at = datetime.datetime.now(tz=pytz.UTC)
            context.reindex()
            request.registry.notify(ActivityExecuted(
                self, [context], get_current()))

        return {}

    def redirect(self, context, request, **kw):
        return nothing


def get_access_key(obj):
    return ['always']


def seeperson_processsecurity_validation(process, context):
    return access_user_processsecurity(process, context)#'active' in context.state


@access_action(access_key=get_access_key)
class SeePerson(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    # style_descriminator = 'access-action'
    # style_interaction = 'ajax-action'
    # style_interaction_type = 'sidebar'
    # style_picto = 'glyphicon glyphicon-eye-open'
    title = _('Details')
    context = IPerson
    actionType = ActionType.automatic
    processsecurity_validation = seeperson_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def reg_roles_validation(process, context):
    return has_role(role=('Anonymous',))


def reg_processsecurity_validation(process, context):
    root = getSite()
    return not getattr(root, 'only_invitation', False)


def remove_expired_preregistration(root, preregistration):
    if preregistration.__parent__ is not None:
        oid = str(get_oid(preregistration))
        root.delfromproperty('preregistrations', preregistration)


def remove_expired_preregistration_callback(root, preregistration):
    remove_expired_preregistration(root, preregistration)
    oid = str(get_oid(preregistration))
    get_socket().send_pyobj(('ack', 'persistent_' + oid))


class Registration(InfiniteCardinality):
    tags = ['main-menu', 'instance']
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = reg_roles_validation
    processsecurity_validation = reg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        preregistration = appstruct['_object_data']
        preregistration.__name__ = gen_random_token()
        preregistration.locale = my_locale_negotiator(request)
        root = getSite()
        root.addtoproperty('preregistrations', preregistration)
        deadline = DEADLINE_PREREGISTRATION * 1000
        oid = get_oid(preregistration)
        call_id = 'persistent_' + str(oid)
        push_callback_after_commit(
            remove_expired_preregistration_callback, deadline, call_id,
            root=root, preregistration=preregistration)
        preregistration.state.append('pending')
        preregistration.reindex()
        transaction.commit()
        if not getattr(root, 'moderate_registration', False):
            accept_preregistration(request, preregistration, root)
        else:
            admins = get_users_with_role(role='SiteAdmin')
            alert(
                'internal', [root], admins,
                internal_kind=InternalAlertKind.admin_alert,
                subjects=[preregistration], alert_kind='new_registration')
            url = request.resource_url(preregistration, '@@index')
            for admin in [a for a in admins if getattr(a, 'email', '')]:
                mail_template = root.get_mail_template(
                    'moderate_preregistration', admin.user_locale)
                subject = mail_template['subject'].format(
                    novaideo_title=root.title)
                email_data = get_user_data(admin, 'recipient', request)
                message = mail_template['template'].format(
                    url=url,
                    novaideo_title=root.title,
                    **email_data)
                alert('email', [root.get_site_sender()], [admin.email],
                      subject=subject, body=message)

        request.registry.notify(ActivityExecuted(self, [preregistration], None))
        return {'preregistration': preregistration}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(
            context, "@@registrationsubmitted"))


def ar_processsecurity_validation(process, context):
    root = getSite()
    return getattr(root, 'moderate_registration', False) and\
        not context.is_expired and\
        global_user_processsecurity()


def ar_roles_validation(process, context):
    organization = getattr(context, 'organization', None)
    if organization:
        return has_any_roles(
            roles=('SiteAdmin', ('OrganizationResponsible', organization)))

    return has_role(role=('SiteAdmin',))


def ar_state_validation(process, context):
    return 'pending' in context.state


class AcceptRegistration(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'primary-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-ok'
    style_order = 1
    submission_title = _('Continue')
    context = IPreregistration
    roles_validation = ar_roles_validation
    processsecurity_validation = ar_processsecurity_validation
    state_validation = ar_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        oid = str(get_oid(context))
        get_socket().send_pyobj(('stop', 'persistent_' + oid))
        context.state = PersistentList(['accepted'])
        accept_preregistration(request, context, root)
        request.registry.notify(ActivityExecuted(self, [context], None))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


class RefuseRegistration(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'primary-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-remove'
    style_order = 2
    submission_title = _('Continue')
    context = IPreregistration
    roles_validation = ar_roles_validation
    processsecurity_validation = ar_processsecurity_validation
    state_validation = ar_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        oid = str(get_oid(context))
        get_socket().send_pyobj(('stop', 'persistent_' + oid))
        remove_expired_preregistration(root, context)
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def confirm_processsecurity_validation(process, context):
    return not context.is_expired


def confirm_state_validation(process, context):
    root = getSite()
    if getattr(root, 'moderate_registration', False):
        return 'accepted' in context.state

    return True


class ConfirmRegistration(InfiniteCardinality):
    submission_title = _('Save')
    context = IPreregistration
    roles_validation = reg_roles_validation
    processsecurity_validation = confirm_processsecurity_validation
    state_validation = confirm_state_validation

    def start(self, context, request, appstruct, **kw):
        data = context.get_data(PersonSchema())
        annotations = getattr(context, 'annotations', {}).get(PROCESS_HISTORY_KEY, [])
        data = {key: value for key, value in data.items()
                if value is not colander.null}
        data.pop('title')
        root = getSite()
        locale = my_locale_negotiator(request)
        data['locale'] = locale
        person = Person(**data)
        principals = find_service(root, 'principals')
        name = person.first_name + ' ' + person.last_name
        users = principals['users']
        name = name_chooser(users, name=name)
        users[name] = person
        grant_roles(person, roles=('Member',))
        grant_roles(person, (('Owner', person),))
        person.state.append('active')
        oid = str(get_oid(context))
        get_socket().send_pyobj(('stop', 'persistent_' + oid))
        organization = context.organization
        if organization:
            person.setproperty('organization', organization)

        root.delfromproperty('preregistrations', context)
        person.init_annotations()
        person.annotations.setdefault(
            PROCESS_HISTORY_KEY, PersistentList()).extend(annotations)
        person.reindex()
        request.registry.notify(ActivityExecuted(self, [person], person))
        root.addtoproperty('news_letter_members', person)
        newsletters = root.get_newsletters_automatic_registration()
        email = getattr(person, 'email', '')
        if newsletters and email:
            for newsletter in newsletters:
                newsletter.subscribe(
                    person.first_name, person.last_name, email)

        transaction.commit()
        if email:
            mail_template = root.get_mail_template(
                'registration_confiramtion', person.user_locale)
            subject = mail_template['subject'].format(
                novaideo_title=root.title)
            recipientdata = get_user_data(person, 'recipient', request)
            message = mail_template['template'].format(
                login_url=request.resource_url(root, '@@login'),
                novaideo_title=root.title,
                **recipientdata)
            alert('email', [root.get_site_sender()], [email],
                  subject=subject, body=message)

        return {'person': person}

    def redirect(self, context, request, **kw):
        return kw['person']


def remind_roles_validation(process, context):
    organization = getattr(context, 'organization', None)
    if organization:
        return has_any_roles(
            roles=('SiteAdmin', ('OrganizationResponsible', organization)))

    return has_role(role=('SiteAdmin',))


def remind_processsecurity_validation(process, context):
    return getattr(context, 'email', '') and \
        global_user_processsecurity()


def remind_state_validation(process, context):
    root = getSite()
    moderate_registration = getattr(root, 'moderate_registration', False)
    if moderate_registration:
        return 'accepted' in context.state

    return True


class Remind(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-refresh'
    style_order = 3
    context = IPreregistration
    submission_title = _('Continue')
    state_validation = remind_state_validation
    roles_validation = remind_roles_validation
    processsecurity_validation = remind_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = request.root
        url = request.resource_url(context, "")
        deadline_date = context.init_deadline(
            datetime.datetime.now(tz=pytz.UTC))
        deadline_str = to_localized_time(
            deadline_date, request, translate=True)
        mail_template = root.get_mail_template(
            'preregistration', getattr(context, 'locale', root.locale))
        email_data = get_user_data(context, 'recipient', request)
        subject = mail_template['subject'].format(
            novaideo_title=root.title)
        deadline_str = to_localized_time(
            deadline_date, request, translate=True)
        message = mail_template['template'].format(
            url=url,
            deadline_date=deadline_str.lower(),
            novaideo_title=root.title,
            **email_data)
        alert('email', [root.get_site_sender()], [context.email],
              subject=subject, body=message)

        request.registry.notify(ActivityExecuted(
            self, [context], get_current()))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def get_access_key_reg(obj):
    organization = getattr(obj, 'organization', None)
    if organization:
        return serialize_roles(
            ('SiteAdmin', 'Admin', ('OrganizationResponsible', obj)))

    return serialize_roles(('SiteAdmin', 'Admin'))


def seereg_processsecurity_validation(process, context):
    has_role_cond = False
    organization = getattr(context, 'organization', None)
    if organization:
        has_role_cond = has_any_roles(
            roles=('SiteAdmin', ('OrganizationResponsible', context)))
    else:
        has_role_cond = has_role(role=('SiteAdmin',))

    return has_role_cond and \
        global_user_processsecurity()


@access_action(access_key=get_access_key_reg)
class SeeRegistration(InfiniteCardinality):
    title = _('Details')
    context = IPreregistration
    actionType = ActionType.automatic
    processsecurity_validation = seereg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seeregs_processsecurity_validation(process, context):
    return has_any_roles(roles=('SiteAdmin', 'OrganizationResponsible')) and \
           global_user_processsecurity()


class SeeRegistrations(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'typcn typcn-user-add'
    style_order = 4
    isSequential = False
    context = INovaIdeoApplication
    processsecurity_validation = seeregs_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context))


class RemoveRegistration(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 5
    submission_title = _('Remove')
    context = IPreregistration
    processsecurity_validation = seereg_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        root.delfromproperty('preregistrations', context)
        return {'root': root}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, '@@seeregistrations'))


def discuss_roles_validation(process, context):
    return has_role(role=('Member',))


def discuss_processsecurity_validation(process, context):
    user = get_current()
    return context is not user and \
        global_user_processsecurity()


def discuss_state_validation(process, context):
    return 'active' in context.state


class Discuss(InfiniteCardinality):
    isSequential = False
    style_descriminator = 'communication-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'sidebar'
    style_interaction_args = 'scroll-bottom'
    style_picto = 'ion-chatbubble'
    style_order = 0
    style_activate = True
    tags = ['primary', 'communication']
    context = IPerson
    roles_validation = discuss_roles_validation
    processsecurity_validation = discuss_processsecurity_validation
    state_validation = discuss_state_validation

    def is_active(self, context, request):
        user = get_current(request)
        channel = context.get_channel(user)
        return True if channel else False

    def get_nb(self, context, request):
        user = get_current(request)
        channel = context.get_channel(user)
        if channel:
            unread_comments = channel.get_comments_between(
                user.get_read_date(channel),
                datetime.datetime.now(tz=pytz.UTC))
            return len(unread_comments)

        return 0

    def get_title(self, context, request, nb_only=False):
        user = get_current()
        channel = context.get_channel(user)
        len_comments = channel.len_comments if channel else 0
        if nb_only:
            return str(len_comments)

        return _("${title} (${number})",
                 mapping={'number': len_comments,
                          'title': request.localizer.translate(self.title)})

    def _get_users_to_alerts(self, context, request, user, channel):
        users = list(channel.members)
        if user in users:
            users.remove(user)

        return users

    def _alert_users(self, context, request, user, comment, channel):
        root = getSite()
        users = self._get_users_to_alerts(context, request, user, channel)
        author_data = get_user_data(user, 'author', request)
        alert_data = get_entity_data(comment, 'comment', request)
        alert_data.update(author_data)
        alert('internal', [root], users,
              internal_kind=InternalAlertKind.comment_alert,
              subjects=[channel],
              comment_kind='discuss',
              **alert_data)
        subject_data = get_entity_data(user, 'subject', request)
        alert_data.update(subject_data)
        for user_to_alert in [u for u in users if getattr(u, 'email', '')]:
            mail_template = root.get_mail_template(
                'alert_discuss', user_to_alert.user_locale)
            subject = mail_template['subject'].format(
                **subject_data)
            email_data = get_user_data(user_to_alert, 'recipient', request)
            email_data.update(alert_data)
            message = mail_template['template'].format(
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [user_to_alert.email],
                  subject=subject, body=message)

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        user = get_current(request)
        channel = context.get_channel(user)
        if not channel:
            channel = PrivateChannel()
            context.addtoproperty('channels', channel)
            channel.addtoproperty('members', user)
            channel.addtoproperty('members', context)
            context.set_read_date(channel, comment.created_at)

        if channel:
            channel.addtoproperty('comments', comment)
            channel.add_comment(comment)
            comment.state = PersistentList(['published'])
            comment.reindex()
            comment.setproperty('author', user)
            grant_roles(user=user, roles=(('Owner', comment), ))
            if appstruct.get('associated_contents', []):
                comment.set_associated_contents(
                    appstruct['associated_contents'], user)

            self._alert_users(context, request, user, comment, channel)
            context.reindex()
            user.set_read_date(channel, datetime.datetime.now(tz=pytz.UTC))

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def gdiscuss_processsecurity_validation(process, context):
    return global_user_processsecurity()


class GeneralDiscuss(InfiniteCardinality):
    isSequential = False
    style_interaction = 'ajax-action'
    style_interaction_type = 'sidebar'
    style_interaction_args = 'scroll-bottom'
    style_picto = 'ion-chatbubble'
    style_order = 0
    style_activate = True
    context = INovaIdeoApplication
    roles_validation = discuss_roles_validation
    processsecurity_validation = gdiscuss_processsecurity_validation

    def get_nb(self, context, request):
        channel = context.channel
        if channel:
            user = get_current()
            if hasattr(user, 'get_read_date'):
                unread_comments = channel.get_comments_between(
                    user.get_read_date(channel),
                    datetime.datetime.now(tz=pytz.UTC))
                return len(unread_comments)

        return 0

    def _get_users_to_alerts(self, context, request, user, channel):
        return 'all'

    def _alert_users(self, context, request, user, comment, channel):
        root = getSite()
        users = self._get_users_to_alerts(context, request, user, channel)
        comment_oid = getattr(comment, '__oid__', 'None')
        authordata = get_user_data(user, 'author', request)
        alert('internal', [root], users, exclude=[user],
              internal_kind=InternalAlertKind.comment_alert,
              subjects=[channel],
              comment_oid=comment_oid,
              comment_content=comment.comment,
              comment_kind='general_discuss',
              **authordata)

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        comment = appstruct['_object_data']
        user = get_current(request)
        mask = user.get_mask(root)
        author = mask if appstruct.get('anonymous', False) and mask else user
        channel = root.channel
        #TODO get
        if channel:
            channel.addtoproperty('comments', comment)
            channel.add_comment(comment)
            comment.state = PersistentList(['published'])
            comment.reindex()
            comment.setproperty('author', author)
            grant_roles(user=author, roles=(('Owner', comment), ))
            if appstruct.get('associated_contents', []):
                comment.set_associated_contents(
                    appstruct['associated_contents'], user)

            self._alert_users(context, request, author, comment, channel)
            context.reindex()
            user.set_read_date(channel, datetime.datetime.now(tz=pytz.UTC))

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class ExtractAlerts(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_picto = 'glyphicon glyphicon-export'
    style_order = 8
    tags = ['secondary', 'entity']
    submission_title = _('Continue')
    context = IPerson
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        user = context
        localizer = request.localizer
        new_alerts = getattr(user, 'alerts', [])
        old_alerts = getattr(user, 'old_alerts', [])
        alerts = []
        for obj in itertools.chain(new_alerts, old_alerts):
            render_dict = {
                'object': obj,
                'current_user': user
            }
            alert = {
                'content': renderers.render(
                    obj.templates['default'],
                    render_dict, request).replace('\n', ''),
                'created_at': to_localized_time(obj.created_at, request, translate=True)
            }
            alerts.append(alert)

        attributes_to_extract = ['created_at', 'content']
        csv_file = StringIO()
        fieldnames = []
        for attr in attributes_to_extract:
            fieldnames.append(
                localizer.translate(EXTRACTION_ATTR[attr]['title']))

        writer = csv.DictWriter(
            csv_file, fieldnames=fieldnames, dialect='excel', delimiter=';')
        writer.writeheader()
        registry = request.registry
        for obj in alerts:
            writer.writerow(
                dict([(localizer.translate(EXTRACTION_ATTR[attr]['title']),
                       obj.get(attr)) for
                      attr in attributes_to_extract]))

        csv_file.seek(0)
        return {'file': BytesIO(csv_file.read().encode('windows-1252', 'replace')), 'user': user}

    def redirect(self, context, request, **kw):
        root = getSite()
        user = kw.get('user', None)
        user_title = getattr(user, 'title', user.name)
        now = datetime.datetime.now()
        date = to_localized_time(now, request=request, translate=True)
        file_name = 'Alerts_Extraction_{user}_{date}_{app}'.format(
            date=date, user=user_title, app=root.title)
        file_name = name_normalizer(file_name.replace(' ', '-'))
        csv_file = kw.get('file', '')
        response = request.response
        response.content_type = 'application/vnd.ms-excel;charset=windows-1252'
        response.content_disposition = 'inline; filename="{file_name}.csv"'.format(
            file_name=file_name)
        response.app_iter = FileIter(csv_file)
        return response


#TODO behaviors

VALIDATOR_BY_CONTEXT[Person] = {
    'action': Discuss,
    'see': SeePerson,
    'access_key': get_access_key
}

VALIDATOR_BY_CONTEXT[NovaIdeoApplication] = {
    'action': GeneralDiscuss,
    'see': None,
    'access_key': None
}
