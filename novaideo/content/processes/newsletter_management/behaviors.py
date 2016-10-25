# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import datetime
import pytz
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound
from pyramid import renderers

from substanced.util import get_oid

from dace.util import getSite, find_catalog
from dace.objectofcollaboration.principal.util import (
    has_role,
    has_any_roles)
from dace.interfaces import IEntity
from dace.processinstance.activity import (
    InfiniteCardinality,
    ActionType)

from novaideo.content.processes.user_management.behaviors import (
    global_user_processsecurity)
from novaideo.content.interface import (
    INovaIdeoApplication,
    INewsletter,
    IProposal,
    Iidea)
from novaideo.core import access_action, serialize_roles
from novaideo import _, nothing
from novaideo.utilities.util import (
    gen_random_token)
from novaideo.utilities.alerts_utility import (
    alert, get_entity_data)
from novaideo.views.filter import find_entities


CONTENT_TEMPLATE = 'novaideo:views/templates/newsletter_content_template.pt'


def get_adapted_content(email, request, last_sending_date=None):
    body = ''
    novaideo_catalog = find_catalog('novaideo')
    identifier_index = novaideo_catalog['identifier']
    query = identifier_index.any([email])
    users = list(query.execute().all())
    member = users[0] if users else None
    query = None
    if last_sending_date:
        published_at_index = novaideo_catalog['published_at']
        query = published_at_index.gt(last_sending_date)

    entities = find_entities(
        interfaces=[IProposal, Iidea],
        metadata_filter={
            'content_types': ['idea', 'proposal'],
            'states': ['published'],
            'keywords': getattr(member, 'keywords', [])},
        sort_on='release_date',
        add_query=query)

    result = []
    for obj in entities:
        result.append(obj)
        if len(result) == 5:
            break

    if result:
        body = renderers.render(
            CONTENT_TEMPLATE, {'entities': result}, request)

    return body


def send_newsletter_content(newsletter, request):
    root = newsletter.__parent__
    subject_base = getattr(newsletter, 'subject', newsletter.title)
    mail_template = newsletter.content
    include_adapted_content = mail_template.find("{content}") >= 0
    sender = root.get_site_sender()
    last_sending_date = getattr(newsletter, 'last_sending_date', None)
    if last_sending_date:
        last_sending_date = datetime.datetime.combine(
            last_sending_date,
            datetime.datetime.min.time()).replace(tzinfo=pytz.UTC)

    for (key, user_data) in newsletter.subscribed.items():
        email = user_data.get('email', None)
        if email:
            content = get_adapted_content(
                email, request, last_sending_date) if \
                include_adapted_content else ''
            if include_adapted_content and not content:
                continue

            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            allow_unsubscribing = getattr(
                newsletter, 'allow_unsubscribing', True)
            unsubscribeurl = request.resource_url(
                root, '@@userunsubscribenewsletter',
                query={'oid': get_oid(newsletter),
                       'user': key+'@@'+user_data.get('id', '')})\
                if allow_unsubscribing \
                else request.resource_url(root, '')
            logo = getattr(root, 'picture', None)
            subject = subject_base.format(
                first_name=first_name,
                last_name=last_name,
                application_title=root.title,
                newsletter_title=newsletter.title,)
            mail = mail_template.format(
                first_name=first_name,
                last_name=last_name,
                application_title=root.title,
                application_url=request.resource_url(root, ''),
                newsletter_title=newsletter.title,
                unsubscribeurl=unsubscribeurl,
                content=content,
                logo=logo.url if logo else\
                    request.static_url('novaideo:static/images/novaideo32.png'))
            alert('email', [sender], [email],
                  subject=subject, html=mail)

    now = datetime.datetime.now(tz=pytz.UTC)
    newsletter.annotations.setdefault(
        'newsletter_history', PersistentList()).append(
        {'date': now,
         'subject': subject_base,
         'content': newsletter.content
        })
    newsletter.content = newsletter.get_content_template()
    newsletter.last_sending_date = now
    if getattr(newsletter, 'recurrence', False):
        newsletter.sending_date = newsletter.get_next_sending_date(now)


def get_access_key(obj):
    result = serialize_roles(('Admin', 'SiteAdmin'))
    return result


def seenewsletter_processsecurity_validation(process, context):
    return has_any_roles(roles=('SiteAdmin',))


@access_action(access_key=get_access_key)
class SeeNewsletter(InfiniteCardinality):
    """SeeFile is the behavior allowing access to context"""
    title = _('Details')
    context = INewsletter
    actionType = ActionType.automatic
    processsecurity_validation = seenewsletter_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def createnewsletter_roles_validation(process, context):
    return has_role(role=('SiteAdmin', ))


def createnewsletter_processsecurity_validation(process, context):
    return global_user_processsecurity()


class CreateNewsletter(InfiniteCardinality):
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-envelope'
    style_order = 5
    title = _('Create a newsletter')
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createnewsletter_roles_validation
    processsecurity_validation = createnewsletter_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        site = getSite()
        newnewsletter = appstruct['_object_data']
        site.addtoproperty('newsletters', newnewsletter)
        newnewsletter.reset_content()
        newnewsletter.init_annotations()
        newnewsletter.reindex()
        return {'newcontext': newnewsletter}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def edit_roles_validation(process, context):
    return has_any_roles(
        roles=('SiteAdmin',))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity()


class EditNewsletter(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = INewsletter
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.reset_content()
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class ConfigureNewsletter(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-wrench'
    style_order = 2
    submission_title = _('Save')
    context = INewsletter
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.sending_date = datetime.datetime.combine(
            context.sending_date,
            datetime.time(0, 0, 0, tzinfo=pytz.UTC))
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class RedactNewsletter(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-align-left'
    style_order = 2
    submission_title = _('Save')
    context = INewsletter
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        # context.reset_content()
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def send_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin',))


def send_processsecurity_validation(process, context):
    return context.validate_content() and \
        global_user_processsecurity()


class SendNewsletter(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-send'
    style_order = 1
    submission_title = _('Continue')
    context = INewsletter
    roles_validation = send_roles_validation
    processsecurity_validation = send_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        send_newsletter_content(context, request)
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def remove_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin',))


def remove_processsecurity_validation(process, context):
    return global_user_processsecurity()


class RemoveNewsletter(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_interaction = 'ajax-action'
    style_order = 10
    submission_title = _('Continue')
    context = INewsletter
    roles_validation = remove_roles_validation
    processsecurity_validation = remove_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        site = getSite()
        site.delfromproperty('newsletters', context)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def subscribe_roles_validation(process, context):
    return has_any_roles(roles=('Anonymous', 'Member'))


def subscribe_processsecurity_validation(process, context):
    site = getSite()
    return site.get_newsletters_for_registration()


class SubscribeNewsletter(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'footer-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-envelope'
    style_order = 4
    submission_title = _('Save')
    context = IEntity
    roles_validation = subscribe_roles_validation
    processsecurity_validation = subscribe_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        email = appstruct.pop('email')
        newnewsletters = appstruct.pop('newsletters')
        first_name = appstruct.get('first_name')
        last_name = appstruct.get('last_name')
        random_key = gen_random_token()
        root = getSite()
        mail_template = root.get_mail_template('newsletter_subscription')
        for newsletter in newnewsletters:
            newsletter.subscribe(first_name, last_name, email, random_key)
            url = request.resource_url(
                context, '@@userunsubscribenewsletter',
                query={'oid': get_oid(newsletter),
                       'user': email+'@@'+random_key})
            email_data = get_entity_data(
                newsletter, 'newsletter', request)
            subject = mail_template['subject'].format(
                newsletter_title=newsletter.title,
                novaideo_title=root.title)
            mail = mail_template['template'].format(
                first_name=first_name,
                last_name=last_name,
                unsubscribeurl=url,
                novaideo_title=root.title,
                **email_data)
            alert('email', [root.get_site_sender()], [email],
                  subject=subject, body=mail)

        return {}

    def redirect(self, context, request, **kw):
        return nothing


def userunsubscribe_roles_validation(process, context):
    return has_any_roles(roles=('Anonymous', 'Member'))


class UserUnsubscribeNewsletter(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-ok'
    style_order = 5
    submission_title = _('Continue')
    context = INovaIdeoApplication
    roles_validation = userunsubscribe_roles_validation

    def start(self, context, request, appstruct, **kw):
        newsletter = appstruct.pop('newsletter')
        user = appstruct.pop('user', None)
        if user and getattr(newsletter, 'allow_unsubscribing', True):
            parts = user.split('@@')
            key = parts[0]
            user_id = parts[1]
            subscribed = newsletter.subscribed.get(key, None)
            if subscribed and user_id == subscribed.get('id', None):
                newsletter.subscribed.pop(key)
                first_name = subscribed.get('first_name')
                last_name = subscribed.get('last_name')
                email = subscribed.get('email')
                root = getSite()
                mail_template = root.get_mail_template(
                    'newsletter_unsubscription')
                email_data = get_entity_data(
                    newsletter, 'newsletter', request)
                subject = mail_template['subject'].format(
                    newsletter_title=newsletter.title,
                    novaideo_title=root.title)
                mail = mail_template['template'].format(
                    first_name=first_name,
                    last_name=last_name,
                    novaideo_title=root.title,
                    **email_data)
                alert('email', [root.get_site_sender()], [email],
                      subject=subject, body=mail)

        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root, ""))


def unsubscribe_processsecurity_validation(process, context):
    return global_user_processsecurity()


def unsubscribe_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin',))


class UnsubscribeNewsletter(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_picto = 'typcn typcn-user-delete'
    style_order = 5
    submission_title = _('Continue')
    context = INewsletter
    roles_validation = unsubscribe_roles_validation
    processsecurity_validation = unsubscribe_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        email = appstruct.pop('email')
        key = email
        subscribed = context.subscribed.get(key, None)
        if subscribed:
            context.subscribed.pop(key)
            first_name = subscribed.get('first_name')
            last_name = subscribed.get('last_name')
            email = subscribed.get('email')
            root = getSite()
            mail_template = root.get_mail_template('newsletter_unsubscription')
            email_data = get_entity_data(context, 'newsletter', request)
            subject = mail_template['subject'].format(
                newsletter_title=context.title,
                novaideo_title=root.title)
            mail = mail_template['template'].format(
                first_name=first_name,
                last_name=last_name,
                novaideo_title=root.title,
                **email_data)
            alert('email', [root.get_site_sender()], [email],
                  subject=subject, body=mail)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def see_all_roles_validation(process, context):
    return has_any_roles(roles=('SiteAdmin',))


def see_all_processsecurity_validation(process, context):
    return context.newsletters and global_user_processsecurity()


class SeeNewsletters(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_picto = 'glyphicon glyphicon-envelope'
    style_order = 4.5
    submission_title = _('Continue')
    context = INovaIdeoApplication
    roles_validation = see_all_roles_validation
    processsecurity_validation = see_all_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def see_subscribed_processsecurity_validation(process, context):
    return context.subscribed and global_user_processsecurity()


class SeeSubscribed(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'ion-person-stalker'
    style_order = 4
    context = INewsletter
    roles_validation = see_all_roles_validation
    processsecurity_validation = see_subscribed_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class SeeNewsletterHistory(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-time'
    title = _('Content history')
    style_order = 2
    isSequential = False
    context = INewsletter
    processsecurity_validation = seenewsletter_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

#TODO behaviors
