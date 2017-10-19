# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS

from novaideo.content.processes.novaideo_view_manager.behaviors import (
    SeeMySupports)
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.views.filter import (
    FILTER_SOURCES)
from .see_my_contents import SeeMyContentsView
from novaideo.views.core import asyn_component_config


CONTENTS_MESSAGES = {
    '0': _(u"""You have evaluated no content so far. You have ${tokens} remaining evaluation tokens"""),
    '1': _(u"""You have evaluated one content so far. You have ${tokens} remaining evaluation tokens"""),
    '*': _(u"""You have evaluated ${number} contents so far. You have ${tokens} remaining evaluation tokens""")
}


@asyn_component_config(id='novaideoapp_seemysupports')
@view_config(
    name='seemysupports',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class SeeMySupportsView(SeeMyContentsView):
    title = _('My evaluations')
    name = 'seemysupports'
    behaviors = [SeeMySupports]
    template = 'novaideo:views/novaideo_view_manager/templates/search_result.pt'
    viewid = 'seemysupports'
    contents_messages = CONTENTS_MESSAGES
    selected_filter = [('metadata_filter', ['negation', 'keywords', 'states', 'challenges']),
                       ('temporal_filter', ['negation', 'created_date']),
                       'text_filter', 'other_filter']
    include_archived = False
    content_types = ['idea', 'proposal']
    display_state = False

    def _get_title(self, **args):
        user = args.get('user')
        return _(self.contents_messages[args.get('index')],
            mapping={'number': args.get('len_result'),
                     'tokens': user.get_len_free_tokens() if hasattr(user, 'get_len_free_tokens') else 0})

    def _get_content_ids(self, user):
        return user.allocated_tokens.keys() if hasattr(user, 'allocated_tokens') else []


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {SeeMySupports: SeeMySupportsView})


FILTER_SOURCES.update(
    {SeeMySupportsView.name: SeeMySupportsView})
