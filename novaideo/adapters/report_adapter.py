# -*- coding: utf8 -*-
# Copyright (c) 2016 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from persistent.list import PersistentList
from zope.interface import Interface, implementer

from dace.util import Adapter, adapter

from novaideo.content.interface import (
    IComment,
    Iidea,
    IProposal)
from novaideo import _
from novaideo.content.processes import get_states_mapping
from novaideo.utilities.alerts_utility import alert
from novaideo.content.alert import InternalAlertKind


class ISignalableObject(Interface):

    def censor(request):
        pass

    def restor(request):
        pass


@adapter(context=IComment)
@implementer(ISignalableObject)
class CommentAdapter(Adapter):
    """Return all keywords.
    """
    def censor(self, request):
        self.context.state = PersistentList(['censored'])
        members = [self.context.author]
        alert(
            'internal', [request.root], members,
            internal_kind=InternalAlertKind.moderation_alert,
            subjects=[self.context], alert_kind='object_censor')

    def restor(self, request):
        self.context.state = PersistentList(['published'])
        members = [self.context.author]
        alert(
            'internal', [request.root], members,
            internal_kind=InternalAlertKind.moderation_alert,
            subjects=[self.context], alert_kind='object_restor')


@adapter(context=Iidea)
@implementer(ISignalableObject)
class IdeaAdapter(Adapter):
    """Return all keywords.
    """
    def censor(self, request):
        self.context.state_befor_censor = PersistentList(
            list(self.context.state))
        self.context.state = PersistentList(['censored'])
        for token in list(self.context.tokens):
            token.owner.addtoproperty('tokens', token)

        members = [self.context.author]
        alert(
            'internal', [request.root], members,
            internal_kind=InternalAlertKind.moderation_alert,
            subjects=[self.context], alert_kind='object_censor')

    def restor(self, request):
        self.context.state = PersistentList(
            list(self.context.state_befor_censor))
        del self.context.state_befor_censor
        members = [self.context.author]
        alert(
            'internal', [request.root], members,
            internal_kind=InternalAlertKind.moderation_alert,
            subjects=[self.context], alert_kind='object_restor')


@adapter(context=IProposal)
@implementer(ISignalableObject)
class ProposalAdapter(Adapter):
    """Return all keywords.
    """
    def censor(self, request):
        self.context.state = PersistentList(['censored'])
        self.context.remove_tokens()
        working_group = self.context.working_group
        working_group.state = PersistentList(['deactivated'])
        working_group.setproperty('wating_list', [])
        members = working_group.members
        alert(
            'internal', [request.root], members,
            internal_kind=InternalAlertKind.moderation_alert,
            subjects=[self.context], alert_kind='object_censor')

    def restor(self, request):
        self.context.state = PersistentList(
            ['open to a working group', 'published'])
        members = [self.context.author]
        alert(
            'internal', [request.root], members,
            internal_kind=InternalAlertKind.moderation_alert,
            subjects=[self.context], alert_kind='object_restor')
