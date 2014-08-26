# -*- coding: utf8 -*-
import datetime
from pyramid.httpexceptions import HTTPFound

from dace.util import (
    getSite,
    getBusinessAction,
    copy,
    find_entities)
from dace.objectofcollaboration.principal.util import has_any_roles, grant_roles, get_current
from dace.processinstance.activity import InfiniteCardinality, ActionType, LimitedCardinality, ElementaryAction

from novaideo.ips.mailer import mailer_send
from novaideo.content.interface import INovaIdeoApplication, IProposal, ICorrelableEntity
from ..user_management.behaviors import global_user_processsecurity
from novaideo.mail import PRESENTATION_PROPOSAL_MESSAGE, PRESENTATION_PROPOSAL_SUBJECT
from novaideo import _
from novaideo.content.proposal import Proposal
from ..comment_management.behaviors import validation_by_context
from novaideo.core import acces_action
from novaideo.content.correlation import Correlation
from novaideo.content.working_group import WorkingGroup


try:
      basestring
except NameError:
      basestring = str


def createproposal_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def createproposal_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


class CreateProposal(ElementaryAction):
    context = INovaIdeoApplication
    roles_validation = createproposal_roles_validation
    processsecurity_validation = createproposal_processsecurity_validation

    def _associate(self, related_ideas, proposal):
        root = getSite()
        datas = {'author': get_current(),
                 'source': proposal,
                 'comment': '',
                 'intention': 'Creation'}
        for idea in related_ideas:
            correlation = Correlation()
            datas['targets'] = [idea]
            correlation.set_data(datas)
            correlation.tags.extend(['related_proposals', 'related_ideas'])
            correlation.type = 1
            root.addtoproperty('correlations', correlation)
            proposal.text = getattr(proposal, 'text', '') + '<div>'+idea.text+'</div>'

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        keywords_ids = appstruct.pop('keywords')
        related_ideas = appstruct.pop('related_ideas')
        
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        proposal = appstruct['_object_data']
        root.addtoproperty('proposals', proposal)
        proposal.setproperty('keywords_ref', result)
        proposal.state.append('draft')
        grant_roles(roles=(('Owner', proposal), ))
        grant_roles(roles=(('Participant', proposal), ))
        proposal.setproperty('author', get_current())
        self.process.execution_context.add_created_entity('proposal', proposal)
        wg = WorkingGroup()
        root.addtoproperty('working_groups', wg)
        wg.setproperty('proposal', proposal)
        wg.addtoproperty('members', get_current())
        wg.state.append('deactivated')
        if related_ideas:
            self._associate(related_ideas, proposal)

        self.newcontext = proposal
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def submit_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def submit_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def submit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def submit_state_validation(process, context):
    return "draft" in context.state


class SubmitProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    relation_validation = submit_relation_validation
    roles_validation = submit_roles_validation
    processsecurity_validation = submit_processsecurity_validation
    state_validation = submit_state_validation


    def start(self, context, request, appstruct, **kw):
        context.state.remove('draft')
        context.state.append('first decision')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

def duplicate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           not ('draft' in context.state)


class DuplicateProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    processsecurity_validation = duplicate_processsecurity_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        copy_of_proposal = copy(context)
        copy_of_proposal.created_at = datetime.datetime.today()
        copy_of_proposal.modified_at = datetime.datetime.today()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        appstruct['keywords_ref'] = result
        copy_of_proposal.set_data(appstruct)
        root.addtoproperty('proposals', copy_of_proposal)
        copy_of_proposal.setproperty('originalentity', context)
        copy_of_proposal.state = ['draft']
        copy_of_proposal.setproperty('author', get_current())
        grant_roles(roles=(('Owner', copy_of_proposal), ))
        self.newcontext = copy_of_proposal
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def edit_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def edit_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))


def edit_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def edit_state_validation(process, context):
    return "draft" in context.state


class EditProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    context = IProposal
    relation_validation = edit_relation_validation
    roles_validation = edit_roles_validation
    processsecurity_validation = edit_processsecurity_validation
    state_validation = edit_state_validation

    def start(self, context, request, appstruct, **kw):
        root = getSite()
        context.modified_at = datetime.datetime.today()
        keywords_ids = appstruct.pop('keywords')
        result, newkeywords = root.get_keywords(keywords_ids)
        for nk in newkeywords:
            root.addtoproperty('keywords', nk)

        result.extend(newkeywords)
        datas = {'keywords_ref': result}
        context.set_data(datas)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))

def pub_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')

def pub_roles_validation(process, context):
    return has_any_roles(roles=(('Owner', context),))

def pub_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and ('amendable' in context.state or 'first decision' in context.state)


class PublishProposal(ElementaryAction):
    style = 'button' #TODO add style abstract class
    context = IProposal
    roles_validation = pub_roles_validation
    relation_validation = pub_relation_validation
    state_validation = pub_state_validation

    def start(self, context, request, appstruct, **kw):
        context.state.remove('draft')
        context.state.append('published')
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def comm_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def comm_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def comm_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def comm_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state


class CommentProposal(InfiniteCardinality):
    isSequential = False
    context = IProposal
    roles_validation = comm_roles_validation
    processsecurity_validation = comm_processsecurity_validation
    state_validation = comm_state_validation

    def start(self, context, request, appstruct, **kw):
        comment = appstruct['_object_data']
        context.addtoproperty('comments', comment)
        user = get_current()
        comment.setproperty('author', user)
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def present_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def present_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def present_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def present_state_validation(process, context):
    return 'published' in context.state


class PresentProposal(InfiniteCardinality):
    context = IProposal
    roles_validation = present_roles_validation
    processsecurity_validation = present_processsecurity_validation
    state_validation = present_state_validation

    def start(self, context, request, appstruct, **kw):
        send_to_me = appstruct['send_to_me']
        members = list(appstruct['members'])
        user = get_current()
        if send_to_me:
            members.append(user)

        user_title=getattr(user, 'user_title','')
        user_first_name=getattr(user, 'first_name', user.name)
        user_last_name=getattr(user, 'last_name','')
        url = request.resource_url(context, "@@index")
        presentation_subject = appstruct['subject']
        presentation_message = appstruct['message']
        subject = presentation_subject.format(proposal_title=context.title)
        for member in members:
            recipient_title = ''
            recipient_first_name = ''
            recipient_last_name = ''
            member_email = ''
            if not isinstance(member, basestring):
                recipient_title = getattr(member, 'user_title','')
                recipient_first_name = getattr(member, 'first_name', member.name)
                recipient_last_name = getattr(member, 'last_name','')
                member_email = member.email
            else:
                member_email = member

            message = presentation_message.format(
                recipient_title=recipient_title,
                recipient_first_name=recipient_first_name,
                recipient_last_name=recipient_last_name,
                proposal_url=url,
                my_title=user_title,
                my_first_name=user_first_name,
                my_last_name=user_last_name
                 )
            mailer_send(subject=subject, recipients=[member_email], body=message)
            if not (member is user):
                context.email_persons_contacted.append(member_email)

        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def associate_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def associate_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def associate_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context) and \
           (has_any_roles(roles=(('Owner', context),)) or \
           (has_any_roles(roles=('Member',)) and not ('draft' in context.state)))

class Associate(InfiniteCardinality):
    context = IProposal
    processsecurity_validation = associate_processsecurity_validation
    roles_validation = associate_roles_validation
    relation_validation = associate_relation_validation

    def start(self, context, request, appstruct, **kw):
        correlation = appstruct['_object_data']
        correlation.setproperty('source', context)
        correlation.setproperty('author', get_current())
        root = getSite()
        root.addtoproperty('correlations', correlation)
        self.newcontext = correlation
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(self.newcontext, "@@index"))


def improve_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def improve_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def improve_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def improve_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class ImproveProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = improve_relation_validation
    roles_validation = improve_roles_validation
    processsecurity_validation = improve_processsecurity_validation
    state_validation = improve_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def correct_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def correct_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def correct_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def correct_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'amendable' in context.state


class CorrectProposal(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = correct_relation_validation
    roles_validation = correct_roles_validation
    processsecurity_validation = correct_processsecurity_validation
    state_validation = correct_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def decision_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def decision_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def decision_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def decision_state_validation(process, context):
    wg = context.working_group
    return 'active' in wg.state and 'first decision' in context.state


def decision_cardinality(process):
    return 3

class FirstPublishDecision(LimitedCardinality):
    isSequential = False
    loopCardinality = decision_cardinality
    context = IProposal
    relation_validation = decision_relation_validation
    roles_validation = decision_roles_validation
    processsecurity_validation = decision_processsecurity_validation
    state_validation = decision_state_validation

    def __init__(self, workitem, **kwargs):
        super(FirstPublishDecision, self).__init__(workitem, **kwargs)
        proposal = self.process.execution_context.created_entity('proposal')
        members = proposal.working_group.members[:3]
        self.local_assigned_to.append(members[self.item])

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def withdraw_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def withdraw_roles_validation(process, context):
    return has_any_roles(roles=('Member',))


def withdraw_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and user in context.working_group.wating_list


def withdraw_state_validation(process, context):
    wg = context.working_group
    return  'amendable' in context.state or 'first decision' in context.state


class Withdraw(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = withdraw_relation_validation
    roles_validation = withdraw_roles_validation
    processsecurity_validation = withdraw_processsecurity_validation
    state_validation = withdraw_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def resign_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def resign_roles_validation(process, context):
    return has_any_roles(roles=(('Participant', context),))


def resign_processsecurity_validation(process, context):
    return global_user_processsecurity(process, context)


def resign_state_validation(process, context):
    wg = context.working_group
    return  'amendable' in context.state


class Resign(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = resign_relation_validation
    roles_validation = resign_roles_validation
    processsecurity_validation = resign_processsecurity_validation
    state_validation = resign_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


def participate_relation_validation(process, context):
    return process.execution_context.has_relation(context, 'proposal')


def participate_roles_validation(process, context):
    return has_any_roles(roles=('Member',)) and not has_any_roles(roles=(('Participant', context),))


def participate_processsecurity_validation(process, context):
    user = get_current()
    return global_user_processsecurity(process, context) and not(user in context.working_group.wating_list)


def participate_state_validation(process, context):
    wg = context.working_group
    return  'amendable' in context.state or 'first decision' in context.state


class Participate(InfiniteCardinality):
    style = 'button' #TODO add style abstract class
    isSequential = False
    context = IProposal
    relation_validation = resign_relation_validation
    roles_validation = resign_roles_validation
    processsecurity_validation = resign_processsecurity_validation
    state_validation = resign_state_validation

    def start(self, context, request, appstruct, **kw):
        #TODO
        return True

    def redirect(self, context, request, **kw):
        return HTTPFound(request.resource_url(context, "@@index"))


#TODO behaviors

validation_by_context[Proposal] = CommentProposal
