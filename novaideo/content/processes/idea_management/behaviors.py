# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the 
Idea management process definition. 
"""
import datetime
from pyramid.httpexceptions import HTTPFound
from persistent.list import PersistentList

from dace.util import (
    getSite,
    getBusinessAction,
    copy)
from dace.objectofcollaboration.principal.util import (
    has_role, 
    grant_roles, 
    get_current)
from dace.processinstance.activity import InfiniteCardinality, ActionType

from novaideo.ips.mailer import mailer_send
from novaideo.mail import (
    ARCHIVEIDEA_SUBJECT, 
    ARCHIVEIDEA_MESSAGE,
    PUBLISHEDIDEA_SUBJECT,
    PUBLISHEDIDEA_MESSAGE)
from novaideo.content.interface import INovaIdeoApplication, Iidea
from ..user_management.behaviors import global_user_processsecurity
from novaideo import _
from novaideo.content.idea import Idea
from ..comment_management.behaviors import VALIDATOR_BY_CONTEXT
from novaideo.core import acces_action
from novaideo.utilities.util import connect
from novaideo.event import ObjectPublished, CorrelableRemoved


try:
    basestring
except NameError:
    basestring = str


def createidea_roles_validation(process, context):
    return has_role(role=('Member',))


def createidea_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class CreateIdea(InfiniteCardinality):
    submission_title = _('Save')
    context = INovaIdeoApplication
    roles_validation = createidea_roles_validation
    processsecurity_validation = createidea_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        idea = appstruct['_object_data']
        root.addtoproperty('ideas', idea)
        idea.setproperty('keywords_ref', result)
        idea.state.append('to work')
        grant_roles(roles=(('Owner', idea), ))
        idea.setproperty('author', get_current())
        idea.reindex()
        return {'newcontext': idea}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def duplicate_processsecurity_validation(process, context):
    return ((has_role(role=('Owner', context)) and \
             (not ('archived' in context.state)) or \
              'version' in context.state) or \
           'published' in context.state) and \
           global_user_processsecurity(process, context) 


class DuplicateIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-resize-full'
    style_order = 5
    submission_title = _('Save')
    context = Iidea
    processsecurity_validation = duplicate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        copy_of_idea = copy(context, (root, 'ideas'))
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        files = [f['_object_data'] for f in appstruct.pop('attached_files')]
        appstruct['attached_files'] = files
        copy_of_idea.setproperty('originalentity', context)
        copy_of_idea.state = PersistentList(['to work'])
        copy_of_idea.setproperty('author', get_current())
        grant_roles(roles=(('Owner', copy_of_idea), ))
        copy_of_idea.set_data(appstruct)
        copy_of_idea.reindex()
        context.reindex()
        return {'newcontext': copy_of_idea}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def del_roles_validation(process, context):
    return has_role(role=('Owner', context))


def del_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def del_state_validation(process, context):
    return 'archived' in context.state and \
            not('version' in context.state)


class DelIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 4
    submission_title = _('Continue')
    context = Iidea
    roles_validation = del_roles_validation
    processsecurity_validation = del_processsecurity_validation
    state_validation = del_state_validation

    def start(self, context, request, appstruct, **kw):
        root  = getSite()
        request.registry.notify(CorrelableRemoved(object=context))
        root.delfromproperty('ideas', context)
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def edit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    return "to work" in context.state


class EditIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = Iidea
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        last_version = context.version
        copy_of_idea = copy(context, 
                        (context, 'version'),
                        new_name=context.__name__,
                        select=('modified_at',), 
                        omit=('created_at',), 
                        roles=True)
        copy_keywords, newkeywords = root.get_keywords(context.keywords)
        copy_of_idea.setproperty('keywords_ref', copy_keywords)
        copy_of_idea.setproperty('version', last_version)
        copy_of_idea.setproperty('originalentity', context.originalentity)
        if last_version is not None:
            grant_roles(roles=(('Owner', last_version), ))

        files = [f['_object_data'] for f in appstruct.pop('attached_files')]
        appstruct['attached_files'] = files
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nkw in newkeywords:
            root.addtoproperty('keywords', nkw)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        copy_of_idea.state = PersistentList(['archived', 'version'])
        
        copy_of_idea.setproperty('author', get_current())
        context.set_data(appstruct)
        context.modified_at = datetime.datetime.today()
        copy_of_idea.reindex()
        context.reindex()
        if 'archived' in context.state:
            recuperate_actions = getBusinessAction(context,
                                                   request,
                                                   'ideamanagement',
                                                   'recuperate')
            if recuperate_actions:
                recuperate_actions[0].execute(context, request, appstruct, **kw)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def submit_roles_validation(process, context):
    return has_role(role=('Owner', context))


def submit_processsecurity_validation(process, context):
    if getattr(context, 'originalentity', None):
        originalentity = getattr(context, 'originalentity')
        if originalentity.text == context.text:
            return False

    return global_user_processsecurity(process, context)


def submit_state_validation(process, context):
    return 'to work' in context.state


class SubmitIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 1
    submission_title = _('Continue')
    context = Iidea
    roles_validation = submit_roles_validation
    processsecurity_validation = submit_processsecurity_validation
    state_validation = submit_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('to work')
        context.state.append('submited')
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def decision_roles_validation(process, context):
    return has_role(role=('Moderator',))


def decision_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def decision_state_validation(process, context):
    return 'submited' in context.state


class ArchiveIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 1
    submission_title = _('Continue')
    context = Iidea
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        explanation = appstruct['explanation']
        context.state.remove('submited')
        context.state.append('archived')
        context.reindex()
        user = context.author
        localizer = request.localizer
        subject = ARCHIVEIDEA_SUBJECT.format(subject_title=context.title)
        message = ARCHIVEIDEA_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(user, 'user_title',''))),
                recipient_first_name=getattr(user, 'first_name', user.name),
                recipient_last_name=getattr(user, 'last_name',''),
                subject_title=context.title,
                subject_url=request.resource_url(context, "@@index"),
                explanation=explanation,
                novaideo_title=request.root.title
                 )
        mailer_send(subject=subject, 
            recipients=[user.email], 
            body=message)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


class PublishIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-share'
    style_order = 1
    submission_title = _('Continue')
    context = Iidea
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = decision_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('submited')
        context.state.append('published')
        context.reindex()
        user = context.author
        localizer = request.localizer
        subject = PUBLISHEDIDEA_SUBJECT.format(subject_title=context.title)
        message = PUBLISHEDIDEA_MESSAGE.format(
                recipient_title=localizer.translate(_(getattr(user, 'user_title',''))),
                recipient_first_name=getattr(user, 'first_name', user.name),
                recipient_last_name=getattr(user, 'last_name',''),
                subject_title=context.title,
                subject_url=request.resource_url(context, "@@index"),
                novaideo_title=request.root.title
                 )
        mailer_send(subject=subject, 
            recipients=[user.email], 
            body=message)
        request.registry.notify(ObjectPublished(object=context))
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))



def ab_roles_validation(process, context):
    return has_role(role=('Owner', context))


def ab_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def ab_state_validation(process, context):
    return 'to work' in context.state


class AbandonIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-stop'
    style_order = 2
    context = Iidea
    roles_validation = ab_roles_validation
    processsecurity_validation = ab_processsecurity_validation
    state_validation = ab_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('to work')
        context.state.append('archived')
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def re_roles_validation(process, context):
    return has_role(role=('Owner', context))


def re_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def re_state_validation(process, context):

    return 'archived' in context.state and \
            not('version' in context.state)


class RecuperateIdea(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_picto = 'glyphicon glyphicon-play'
    style_order = 3
    context = Iidea
    roles_validation = re_roles_validation
    processsecurity_validation = re_processsecurity_validation
    state_validation = re_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('archived')
        context.state.append('to work')
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_roles_validation(process, context):
    return has_role(role=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    return 'published' in context.state


class CommentIdea(InfiniteCardinality):
    isSequential = False
    context = Iidea
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        user = get_current()
        comment.setproperty('author', user)
        if appstruct['related_contents']['associate']:
            related_contents = appstruct['related_contents']['related_contents']
            correlation = connect(context, 
                             list(related_contents),
                             {'comment': comment.comment,
                              'type': comment.intention},
                              user,
                              unique=True)
            comment.setproperty('related_correlation', correlation)

        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def present_roles_validation(process, context):
    return has_role(role=('Member',))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def present_state_validation(process, context):
    return 'published' in context.state


class PresentIdea(InfiniteCardinality):
    submission_title = _('Send')
    context = Iidea
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation

    def start(self, context, request, appstruct, **kw):
        send_to_me = appstruct['send_to_me']
        members = list(appstruct['members'])
        user = get_current()
        if send_to_me:
            members.append(user)

        localizer = request.localizer
        user_title = localizer.translate(_(getattr(user, 'user_title','')))
        user_first_name = getattr(user, 'first_name', user.name)
        user_last_name = getattr(user, 'last_name','')
        url = request.resource_url(context, "@@index")
        presentation_subject = appstruct['subject']
        presentation_message = appstruct['message']
        subject = presentation_subject.format(subject_title=context.title)
        for member in members:
            recipient_title = ''
            recipient_first_name = ''
            recipient_last_name = ''
            member_email = ''
            if not isinstance(member, basestring):
                recipient_title = localizer.translate(_(getattr(member, 'user_title','')))
                recipient_first_name = getattr(member, 'first_name', member.name)
                recipient_last_name = getattr(member, 'last_name','')
                member_email = member.email
            else:
                member_email = member

            message = presentation_message.format(
                recipient_title=recipient_title,
                recipient_first_name=recipient_first_name,
                recipient_last_name=recipient_last_name,
                subject_url=url,
                subject_title=getattr(context, 'title', context.name),
                my_title=user_title,
                my_first_name=user_first_name,
                my_last_name=user_last_name,
                novaideo_title=request.root.title
                 )
            mailer_send(subject=subject,
                  recipients=[member_email],
                  body=message)
            if not (member is user):
                context._email_persons_contacted.append(member_email)

        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def associate_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or \
           (has_role(role=('Member',)) and 'published' in context.state)) and \
           global_user_processsecurity(process, context) 



class Associate(InfiniteCardinality):
    context = Iidea
    processsecurity_validation = associate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        correlation = appstruct['_object_data']
        correlation.setproperty('source', context)
        correlation.setproperty('author', get_current())
        root = getSite()
        root.addtoproperty('correlations', correlation)
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def seeidea_processsecurity_validation(process, context):
    return ('published' in context.state or has_role(role=('Owner', context))) or \
           ('submited' in context.state or has_role(role=('Moderator',))) 


@acces_action()
class SeeIdea(InfiniteCardinality):
    """SeeIdea is the behavior allowing access to context"""
    title = _('Details')
    context = Iidea
    actionType = ActionType.automatic
    processsecurity_validation = seeidea_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def compare_roles_validation(process, context):
    return has_role(role=('Owner', context))


def compare_processsecurity_validation(process, context):
    return getattr(context, 'version', None) is not None


class CompareIdea(InfiniteCardinality):
    title = _('Compare')
    context = Iidea
    roles_validation = compare_roles_validation
    processsecurity_validation = compare_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors

VALIDATOR_BY_CONTEXT[Idea] = CommentIdea
