# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Question management process definition.
"""
import datetime
import pytz
import transaction
from persistent.list import PersistentList
from pyramid.httpexceptions import HTTPFound

from dace.util import getSite
from dace.objectofcollaboration.principal.util import (
    has_role,
    has_any_roles,
    grant_roles,
    get_current)
from dace.processinstance.activity import InfiniteCardinality, ActionType
from dace.processinstance.core import ActivityExecuted

from novaideo.content.interface import (
    INovaIdeoApplication, IQuestion, IAnswer)
from ..user_management.behaviors import (
    global_user_processsecurity,
    access_user_processsecurity)
from novaideo import _, nothing
from novaideo.content.question import Question
from novaideo.content.question import Answer
from ..comment_management import VALIDATOR_BY_CONTEXT
from novaideo.core import access_action, serialize_roles
from novaideo.event import (
    CorrelableRemoved, ObjectPublished)
from novaideo.utilities.alerts_utility import (
    alert, get_user_data, get_entity_data, alert_comment_nia)
from novaideo.content.alert import InternalAlertKind
from novaideo.content.comment import Comment
from novaideo.content.processes.idea_management.behaviors import (
    PresentIdea,
    CommentIdea,
    Associate as AssociateIdea)
from novaideo.content.processes.idea_management.behaviors import CreateIdea
from novaideo.views.filter import get_users_by_preferences
from novaideo.content.correlation import CorrelationType
from novaideo.utilities.util import connect


def createquestion_roles_validation(process, context):
    return has_role(role=('Member',))


def createquestion_processsecurity_validation(process, context):
    return global_user_processsecurity()


class AskQuestion(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'admin-action'
    style_interaction = 'ajax-action'
    style_picto = 'md md-live-help'
    style_order = 0
    title = _('Ask a question')
    unavailable_link = 'docanonymous'
    submission_title = _('Ask')
    context = INovaIdeoApplication
    roles_validation = createquestion_roles_validation
    processsecurity_validation = createquestion_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current(request)
        question = appstruct['_object_data']
        root.merge_keywords(question.keywords)
        root.addtoproperty('questions', question)
        question.state.extend(['pending', 'published'])
        grant_roles(user=user, roles=(('Owner', question), ))
        question.setproperty('author', user)
        if isinstance(context, Comment):
            related_contents = [question]
            content = context.subject
            correlations = connect(
                content,
                list(related_contents),
                {'comment': context.comment,
                 'type': context.intention},
                user,
                ['transformation'],
                CorrelationType.solid)
            for correlation in correlations:
                correlation.setproperty('context', context)

            context_type = context.__class__.__name__.lower()
            # Add Nia comment
            alert_comment_nia(
                question, request, root,
                internal_kind=InternalAlertKind.content_alert,
                subject_type='question',
                alert_kind='transformation',
                content=context
                )

            # Add Nia comment
            alert_comment_nia(
                context, request, root,
                internal_kind=InternalAlertKind.content_alert,
                subject_type=context_type,
                alert_kind='transformation_question',
                question=question
                )

        question.format(request)
        question.reindex()
        request.registry.notify(ActivityExecuted(self, [question], user))
        request.registry.notify(ObjectPublished(object=question))
        return {'newcontext': question}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(kw['newcontext'], "@@index"))


def del_roles_validation(process, context):
    return has_any_roles(roles=('Moderator', ))


def del_processsecurity_validation(process, context):
    return global_user_processsecurity()


def del_state_validation(process, context):
    return 'archived' in context.state


class DelQuestion(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 6
    submission_title = _('Continue')
    context = IQuestion
    roles_validation = del_roles_validation
    processsecurity_validation = del_processsecurity_validation
    state_validation = del_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        request.registry.notify(CorrelableRemoved(object=context))
        root.delfromproperty('questions', context)
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def edit_roles_validation(process, context):
    return has_role(role=('Moderator',))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity()


def edit_state_validation(process, context):
    return "pending" in context.state


class EditQuestion(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IQuestion
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        user = get_current(request)
        files = [f['_object_data'] for f in appstruct.pop('attached_files')]
        appstruct['attached_files'] = files
        root.merge_keywords(appstruct['keywords'])
        context.set_data(appstruct)
        context.modified_at = datetime.datetime.now(tz=pytz.UTC)
        context.format(request)
        context.reindex()
        request.registry.notify(ActivityExecuted(self, [context], user))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def decision_roles_validation(process, context):
    return has_role(role=('Moderator',))


def decision_processsecurity_validation(process, context):
    return global_user_processsecurity()


class ArchiveQuestion(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'plus-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-inbox'
    style_order = 4
    submission_title = _('Continue')
    context = IQuestion
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        explanation = appstruct['explanation']
        context.state = PersistentList(['archived'])
        context.reindex()
        user = context.author
        alert('internal', [root], [user],
              internal_kind=InternalAlertKind.moderation_alert,
              subjects=[context], alert_kind='object_archive')
        if getattr(user, 'email', ''):
            mail_template = root.get_mail_template('archive_content_decision')
            subject = mail_template['subject'].format(
                subject_title=context.title)
            email_data = get_user_data(user, 'recipient', request)
            email_data.update(get_entity_data(context, 'subject', request))
            message = mail_template['template'].format(
                explanation=explanation,
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [user.email],
                  subject=subject, body=message)

        return {}

    def redirect(self, context, request, **kw):
        return nothing


def answer_roles_validation(process, context):
    return has_role(role=('Member',))


def answer_processsecurity_validation(process, context):
    options = getattr(context, 'options', [])
    options_condition = True
    if options:
        user = get_current()
        if context.get_selected_option(user) is not None:
            options_condition = False

    return options_condition and global_user_processsecurity()


def answer_state_validation(process, context):
    return 'pending' in context.state


class AnswerQuestion(InfiniteCardinality):
    isSequential = False
    style_descriminator = 'communication-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'inline'
    style_picto = 'ion-chatbubble'
    style_order = 0
    style_activate = True
    context = IQuestion
    roles_validation = answer_roles_validation
    processsecurity_validation = answer_processsecurity_validation
    state_validation = answer_state_validation

    def get_nb(self, context, request):
        return context.len_answers

    def get_title(self, context, request, nb_only=False):
        len_answers = context.len_answers
        if nb_only:
            return str(len_answers)

        return _("${title} (${nember})",
                 mapping={'nember': len_answers,
                          'title': request.localizer.translate(self.title)})

    def _get_users_to_alerts(self, context, request):
        #@TODO OPTIMIZATION
        author = getattr(context, 'author', None)
        users = list(get_users_by_preferences(context))
        if author not in users:
            users.append(author)

        return users

    def _alert_users(self, context, request, user, answer):
        root = getSite()
        users = self._get_users_to_alerts(context, request)
        if user in users:
            users.remove(user)

        mail_template = root.get_mail_template('alert_answer')
        author_data = get_user_data(user, 'author', request)
        alert_data = get_entity_data(answer, 'comment', request)
        alert_data.update(author_data)
        alert('internal', [root], users,
              internal_kind=InternalAlertKind.content_alert,
              alert_kind='new_answer',
              subjects=[context],
              **alert_data)
        subject_data = get_entity_data(context, 'subject', request)
        alert_data.update(subject_data)
        subject = mail_template['subject'].format(
            **subject_data)
        for user_to_alert in [u for u in users if getattr(u, 'email', '')]:
            email_data = get_user_data(user_to_alert, 'recipient', request)
            email_data.update(alert_data)
            message = mail_template['template'].format(
                novaideo_title=root.title,
                **email_data
            )
            alert('email', [root.get_site_sender()], [user_to_alert.email],
                  subject=subject, body=message)

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        answer = appstruct['_object_data']
        context.addtoproperty('answers', answer)
        answer.init_title()
        answer.format(request)
        answer.state = PersistentList(['published'])
        answer.reindex()
        if getattr(answer, 'option', None) is not None:
            answer.question.add_selected_option(user, answer.option)

        transaction.commit()
        grant_roles(user=user, roles=(('Owner', answer), ))
        answer.setproperty('author', user)
        if appstruct.get('associated_contents', []):
            answer.set_associated_contents(
                appstruct['associated_contents'], user)

        self._alert_users(context, request, user, answer)
        context.reindex()
        user.set_read_date(answer.channel, datetime.datetime.now(tz=pytz.UTC))
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def answera_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def answera_processsecurity_validation(process, context):
    return True


class AnswerQuestionAnonymous(AnswerQuestion):
    roles_validation = answera_roles_validation
    processsecurity_validation = answera_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def comm_roles_validation(process, context):
    return has_role(role=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity()


def comm_state_validation(process, context):
    return 'published' in context.state


class CommentQuestion(CommentIdea):
    context = IQuestion
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation
    style_order = 1


def comma_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def comma_processsecurity_validation(process, context):
    return True


class CommentQuestionAnonymous(CommentQuestion):
    roles_validation = comma_roles_validation
    processsecurity_validation = comma_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def present_roles_validation(process, context):
    return has_role(role=('Member',))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity()


def present_state_validation(process, context):
    return 'published' in context.state


class PresentQuestion(PresentIdea):
    context = IQuestion
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation
    style_order = 2


def presenta_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def presenta_processsecurity_validation(process, context):
    return True


class PresentQuestionAnonymous(PresentQuestion):
    roles_validation = presenta_roles_validation
    processsecurity_validation = presenta_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def associate_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or \
           (has_role(role=('Member',)) and 'published' in context.state)) and \
           global_user_processsecurity()


class Associate(AssociateIdea):
    context = IQuestion
    processsecurity_validation = associate_processsecurity_validation


def get_access_key(obj):
    if 'published' in obj.state:
        challenge = getattr(obj, 'challenge', None)
        is_restricted = getattr(challenge, 'is_restricted', False)
        if is_restricted:
            return serialize_roles(
                (('ChallengeParticipant', challenge),
                 'SiteAdmin', 'Admin', 'Moderator'))

        return ['always']
    else:
        return serialize_roles(
            (('Owner', obj), 'SiteAdmin', 'Admin', 'Moderator'))


def seequestion_processsecurity_validation(process, context):
    challenge = getattr(context, 'challenge', None)
    is_restricted = getattr(challenge, 'is_restricted', False)
    can_access = True
    if is_restricted:
        can_access = has_role(role=('ChallengeParticipant', challenge))

    return can_access and access_user_processsecurity(process, context) and \
           ('published' in context.state or 'censored' in context.state or\
            has_any_roles(roles=(('Owner', context), 'Moderator')))


@access_action(access_key=get_access_key)
class SeeQuestion(InfiniteCardinality):
    """SeeQuestion is the behavior allowing access to context"""
    style = 'button' #TODO add style abstract class
    style_descriminator = 'access-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'sidebar'
    style_picto = 'glyphicon glyphicon-eye-open'
    title = _('Details')
    context = IQuestion
    actionType = ActionType.automatic
    processsecurity_validation = seequestion_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def support_roles_validation(process, context):
    return has_role(role=('Member',))


def support_processsecurity_validation(process, context):
    user = get_current()
    return not context.has_positive_vote(user) and global_user_processsecurity()


def support_state_validation(process, context):
    return 'published' in context.state


class SupportQuestion(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    style_descriminator = 'support-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    # style_picto = 'glyphicon glyphicon-thumbs-up'
    # style_order = 4
    context = IQuestion
    roles_validation = support_roles_validation
    processsecurity_validation = support_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        context.withdraw_vote(user)
        context.add_vote(
            user,
            datetime.datetime.now(tz=pytz.UTC))
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def supportqan_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def supportqan_processsecurity_validation(process, context):
    return True


class SupportQuestionAnonymous(SupportQuestion):
    roles_validation = supportqan_roles_validation
    processsecurity_validation = supportqan_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def oppose_processsecurity_validation(process, context):
    user = get_current()
    return not context.has_negative_vote(user) and global_user_processsecurity()


class OpposeQuestion(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    style_descriminator = 'support-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    # style_picto = 'glyphicon glyphicon-thumbs-down'
    # style_order = 5
    context = IQuestion
    roles_validation = support_roles_validation
    processsecurity_validation = oppose_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        context.withdraw_vote(user)
        context.add_vote(
            user,
            datetime.datetime.now(tz=pytz.UTC),
            'negative')
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


class OpposeQuestionAnonymous(OpposeQuestion):
    roles_validation = supportqan_roles_validation
    processsecurity_validation = supportqan_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def withdrawt_processsecurity_validation(process, context):
    user = get_current()
    return context.has_vote(user) and global_user_processsecurity()


class WithdrawToken(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    style_descriminator = 'support-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    # style_picto = 'glyphicon glyphicon-share-alt'
    # style_order = 6
    context = IQuestion
    roles_validation = support_roles_validation
    processsecurity_validation = withdrawt_processsecurity_validation
    state_validation = support_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        context.withdraw_vote(user)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def close_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context), 'Moderator'))


def close_processsecurity_validation(process, context):
    options = getattr(context, 'options', [])
    return options and global_user_processsecurity()


def close_state_validation(process, context):
    return 'pending' in context.state


class Close(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'primary-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-off'
    style_order = 0
    context = IQuestion
    submission_title = _('Continue')
    roles_validation = close_roles_validation
    processsecurity_validation = close_processsecurity_validation
    state_validation = close_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state = PersistentList(['closed', 'published'])
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing

#TODO behaviors

VALIDATOR_BY_CONTEXT[Question] = {
    'action': CommentQuestion,
    'see': SeeQuestion,
    'access_key': get_access_key
}

# Answers


def dela_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context), 'Moderator'))


def dela_processsecurity_validation(process, context):
    return global_user_processsecurity()


def dela_state_validation(process, context):
    return 'archived' in context.state


class DelAnswer(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'global-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-trash'
    style_order = 6
    submission_title = _('Continue')
    context = IAnswer
    roles_validation = del_roles_validation
    processsecurity_validation = del_processsecurity_validation
    state_validation = dela_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current()
        question = context.question
        if getattr(context, 'option', None) is not None:
            question.remove_selected_option(user)

        request.registry.notify(CorrelableRemoved(object=context))
        question.delfromproperty('answers', context)
        return {}

    def redirect(self, context, request, **kw):
        root = getSite()
        return HTTPFound(request.resource_url(root))


def edita_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context), 'Moderator'))


def edita_processsecurity_validation(process, context):
    return global_user_processsecurity()


def edita_state_validation(process, context):
    return 'pending' in context.question.state


class EditAnswer(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'text-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'inline'
    style_picto = 'glyphicon glyphicon-pencil'
    style_order = 1
    submission_title = _('Save')
    context = IAnswer
    roles_validation = edita_roles_validation
    processsecurity_validation = edita_processsecurity_validation
    state_validation = edita_state_validation

    def start(self, context, request, appstruct, **kw):
        context.edited = True
        user = get_current()
        if getattr(context, 'option', None) is not None:
            context.question.add_selected_option(user, context.option)

        if appstruct.get('associated_contents', []):
            context.set_associated_contents(
                appstruct['associated_contents'], user)

        context.format(request)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


class ArchiveAnswer(ArchiveQuestion):
    context = IAnswer


class CommentAnswer(CommentIdea):
    context = IAnswer
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation
    subscribe_to_channel = False


class PresentAnswer(PresentIdea):
    context = IAnswer
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation


class CommentAnswerAnonymous(CommentAnswer):
    roles_validation = comma_roles_validation
    processsecurity_validation = comma_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


class PresentAnswerAnonymous(PresentAnswer):
    roles_validation = presenta_roles_validation
    processsecurity_validation = presenta_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def associatea_processsecurity_validation(process, context):
    return (has_role(role=('Owner', context)) or \
           (has_role(role=('Member',)) and 'published' in context.state)) and \
           global_user_processsecurity()


class AssociateAnswer(AssociateIdea):
    context = IAnswer
    processsecurity_validation = associatea_processsecurity_validation


def get_access_key_answer(obj):
    if 'published' in obj.state:
        return ['always']
    else:
        return serialize_roles(
            (('Owner', obj), 'SiteAdmin', 'Admin', 'Moderator'))


def seeanswer_processsecurity_validation(process, context):
    return access_user_processsecurity(process, context) and \
           ('published' in context.state or 'censored' in context.state or\
            has_any_roles(roles=(('Owner', context), 'Moderator')))


@access_action(access_key=get_access_key_answer)
class SeeAnswer(InfiniteCardinality):
    """SeeAnswer is the behavior allowing access to context"""
    style = 'button' #TODO add style abstract class
    style_descriminator = 'access-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'sidebar'
    style_picto = 'glyphicon glyphicon-eye-open'
    title = _('Details')
    context = IAnswer
    actionType = ActionType.automatic
    processsecurity_validation = seeanswer_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        return {}

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def supporta_roles_validation(process, context):
    return has_role(role=('Member',))


def supporta_processsecurity_validation(process, context):
    user = get_current()
    return not context.has_positive_vote(user) and global_user_processsecurity()


def supporta_state_validation(process, context):
    return 'published' in context.question.state


class SupportAnswer(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    style_descriminator = 'support-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    # style_picto = 'glyphicon glyphicon-thumbs-up'
    # style_order = 4
    context = IAnswer
    roles_validation = supporta_roles_validation
    processsecurity_validation = supporta_processsecurity_validation
    state_validation = supporta_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        context.withdraw_vote(user)
        context.add_vote(
            user,
            datetime.datetime.now(tz=pytz.UTC))
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def supportan_roles_validation(process, context):
    return has_role(role=('Anonymous',), ignore_superiors=True)


def supportan_processsecurity_validation(process, context):
    return True


class SupportAnswerAnonymous(SupportAnswer):
    roles_validation = supportan_roles_validation
    processsecurity_validation = supportan_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def opposea_processsecurity_validation(process, context):
    user = get_current()
    return not context.has_negative_vote(user) and global_user_processsecurity()


class OpposeAnswer(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    style_descriminator = 'support-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    # style_picto = 'glyphicon glyphicon-thumbs-down'
    # style_order = 5
    context = IAnswer
    roles_validation = supporta_roles_validation
    processsecurity_validation = opposea_processsecurity_validation
    state_validation = supporta_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        context.withdraw_vote(user)
        context.add_vote(
            user,
            datetime.datetime.now(tz=pytz.UTC),
            'negative')
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


class OpposeAnswerAnonymous(OpposeAnswer):
    roles_validation = supportan_roles_validation
    processsecurity_validation = supportan_processsecurity_validation
    style_interaction = 'ajax-action'
    style_interaction_type = 'popover'

    def start(self, context, request, appstruct, **kw):
        return {}


def withdrawta_processsecurity_validation(process, context):
    user = get_current()
    return context.has_vote(user) and global_user_processsecurity()


class WithdrawTokenAnswer(InfiniteCardinality):
    # style = 'button' #TODO add style abstract class
    style_descriminator = 'support-action'
    style_interaction = 'ajax-action'
    style_interaction_type = 'direct'
    # style_picto = 'glyphicon glyphicon-share-alt'
    # style_order = 6
    context = IAnswer
    roles_validation = supporta_roles_validation
    processsecurity_validation = withdrawta_processsecurity_validation
    state_validation = supporta_state_validation

    def start(self, context, request, appstruct, **kw):
        user = get_current(request)
        context.withdraw_vote(user)
        context.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def validate_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context), 'Moderator'))


def validate_processsecurity_validation(process, context):
    options = getattr(context.question, 'options', [])
    return not options and global_user_processsecurity()


def validate_state_validation(process, context):
    return 'pending' in context.question.state and 'published' in context.state


class ValidateAnswer(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'primary-action'
    style_interaction = 'ajax-action'
    style_picto = 'glyphicon glyphicon-ok'
    style_order = 0
    context = IAnswer
    submission_title = _('Continue')
    roles_validation = validate_roles_validation
    processsecurity_validation = validate_processsecurity_validation
    state_validation = validate_state_validation

    def start(self, context, request, appstruct, **kw):
        question = context.question
        question.state = PersistentList(['closed', 'published'])
        context.state = PersistentList(['validated', 'published'])
        question.setproperty('answer', context)
        context.reindex()
        question.reindex()
        return {}

    def redirect(self, context, request, **kw):
        return nothing


def state_validation(process, context):
    return 'published' in context.state


class TransformToIdea(CreateIdea):
    style = 'button' #TODO add style abstract class
    style_descriminator = 'primary-action'
    style_interaction = 'ajax-action'
    style_picto = 'icon novaideo-icon icon-idea'
    style_order = 3
    title = _('Transform into an idea')
    context = IAnswer
    state_validation = state_validation


#TODO behaviors

VALIDATOR_BY_CONTEXT[Answer] = {
    'action': CommentAnswer,
    'see': SeeAnswer,
    'access_key': get_access_key_answer
}
