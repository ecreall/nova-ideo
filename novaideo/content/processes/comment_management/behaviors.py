# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Comment management process definition.
"""
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from dace.processinstance.activity import InfiniteCardinality

from novaideo.content.interface import IComment
from novaideo import _
from novaideo.utilities.util import connect
from novaideo.utilities.alerts_utility import alert
from novaideo.content.alert import InternalAlertKind


VALIDATOR_BY_CONTEXT = {}


def respond_relation_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in VALIDATOR_BY_CONTEXT:
            comment_action = VALIDATOR_BY_CONTEXT[subject.__class__]
            return comment_action.relation_validation.__func__(process, subject)
    except Exception:
        return True


def respond_roles_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in VALIDATOR_BY_CONTEXT:
            comment_action = VALIDATOR_BY_CONTEXT[subject.__class__]
            return comment_action.roles_validation.__func__(process, subject)
    except Exception:
        return True


def respond_processsecurity_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in VALIDATOR_BY_CONTEXT:
            comment_action = VALIDATOR_BY_CONTEXT[subject.__class__]
            return comment_action.processsecurity_validation.__func__(
                process, subject)
    except Exception:
        return True


def respond_state_validation(process, context):
    subject = context.subject
    try:
        if subject.__class__ in VALIDATOR_BY_CONTEXT:
            comment_action = VALIDATOR_BY_CONTEXT[subject.__class__]
            return comment_action.state_validation.__func__(process, subject)
    except Exception:
        return True


class Respond(InfiniteCardinality):
    style_picto = 'ion-chatbubbles'
    title = _('Replay')
    access_controled = True
    context = IComment
    relation_validation = respond_relation_validation
    roles_validation = respond_roles_validation
    processsecurity_validation = respond_processsecurity_validation
    state_validation = respond_state_validation

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        comment.format(request)
        user = get_current()
        comment.setproperty('author', user)
        content = comment.subject
        channel = comment.channel
        is_discuss = channel.is_discuss()
        if appstruct['related_contents']:
            related_contents = appstruct['related_contents']
            correlation = connect(
                content,
                list(related_contents),
                {'comment': comment.comment,
                 'type': comment.intention},
                user,
                unique=True)
            comment.setproperty('related_correlation', correlation)

        author = getattr(content, 'author', None)
        authors = getattr(content, 'authors', [author] if author else [])
        comment_author = getattr(context, 'author', None)

        if user in authors:
            authors.remove(user)

        if comment_author in authors:
            authors.remove(comment_author)

        root = getSite()
        comment_oid = getattr(comment, '__oid__', 'None')
        localizer = request.localizer
        author_title = localizer.translate(
            _(getattr(comment_author, 'user_title', '')))
        author_first_name = getattr(
            comment_author, 'first_name', comment_author.name)
        author_last_name = getattr(comment_author, 'last_name', '')
        comment_kind = 'discuss' if is_discuss else 'comment'
        alert('internal', [root], authors,
              internal_kind=InternalAlertKind.comment_alert,
              subjects=[content],
              comment_oid=comment_oid,
              author_title=author_title,
              author_first_name=author_first_name,
              author_last_name=author_last_name,
              comment_kind=comment_kind)
        mail_template = root.get_mail_template(
            'alert_discuss' if is_discuss else 'alert_comment')
        subject_type = localizer.translate(
            _("The " + content.__class__.__name__.lower()))
        subject = mail_template['subject'].format(
            subject_title=content.title,
            subject_type=subject_type)
        for user_to_alert in [u for u in authors if getattr(u, 'email', '')]:
            message = mail_template['template'].format(
                recipient_title=localizer.translate(
                    _(getattr(user_to_alert, 'user_title', ''))),
                recipient_first_name=getattr(
                    user_to_alert, 'first_name', user_to_alert.name),
                recipient_last_name=getattr(user_to_alert, 'last_name', ''),
                subject_title=content.title,
                subject_url=request.resource_url(content, "@@index") + '#comment-' + str(comment_oid),
                subject_type=subject_type,
                author_title=author_title,
                author_first_name=author_first_name,
                author_last_name=author_last_name,
                novaideo_title=root.title
            )
            alert('email', [root.get_site_sender()], [user_to_alert.email],
                  subject=subject, body=message)

        if comment_author is not user:
            alert('internal', [root], [comment_author],
                  internal_kind=InternalAlertKind.comment_alert,
                  subjects=[content], is_respons=True,
                  author_title=author_title,
                  comment_oid=comment_oid,
                  author_first_name=author_first_name,
                  author_last_name=author_last_name,
                  comment_kind=comment_kind
                  )
            if getattr(comment_author, 'email', ''):
                mail_template = root.get_mail_template(
                    'alert_discuss' if is_discuss else 'alert_respons')
                subject = mail_template['subject'].format(
                    subject_title=content.title,
                    subject_type=subject_type)
                message = mail_template['template'].format(
                    recipient_title=localizer.translate(
                        _(getattr(comment_author, 'user_title', ''))),
                    recipient_first_name=getattr(
                        comment_author, 'first_name', comment_author.name),
                    recipient_last_name=getattr(
                        comment_author, 'last_name', ''),
                    subject_title=content.title,
                    subject_url=request.resource_url(content, "@@index") + '#comment-' + str(comment_oid),
                    subject_type=subject_type,
                    author_title=author_title,
                    author_first_name=author_first_name,
                    author_last_name=author_last_name,
                    novaideo_title=root.title
                )
                alert('email', [root.get_site_sender()], [comment_author.email],
                      subject=subject, body=message)

        return {'newcontext': comment.subject}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], '@@index'))


#TODO behaviors
