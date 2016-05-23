# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeMyParticipations)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.views.filter import (
    FILTER_SOURCES)
from .see_my_contents import SeeMyContentsView


CONTENTS_MESSAGES = {
    '0': _(u"""Aucune participations"""),
    '1': _(u"""Un groupe de travail auquel j'ai participé"""),
    '*': _(u"""${nember} groupes de travail auxquels j'ai participé""")
}


@view_config(
    name='seemyparticipations',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeMyParticipationsView(SeeMyContentsView):
    title = _('My participations')
    name = 'seemyparticipations'
    behaviors = [SeeMyParticipations]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seemyparticipations'
    contents_messages = CONTENTS_MESSAGES
    selected_filter = [('metadata_filter', ['keywords', 'states']),
                       ('temporal_filter', ['negation', 'created_date']),
                       'text_filter', 'other_filter']
    include_archived = False

    def _get_content_ids(self, user):
        return [get_oid(o) for o in getattr(user, 'participations', [])]


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeMyParticipations: SeeMyParticipationsView})


FILTER_SOURCES.update(
    {SeeMyParticipationsView.name: SeeMyParticipationsView})
