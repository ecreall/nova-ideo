# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.view import BasicView
from pontus.form import FormView
from pontus.schema import select, Schema

from novaideo.content.processes.novaideo_abstract_process.behaviors import (
    AddReaction)
from novaideo.core import Emojiable
from novaideo import _
from novaideo.widget import EmojiInputWidget


DEFAULT_REACTION = []#[':+1:', ':-1:']


@colander.deferred
def reaction_widget(node, kw):
    return EmojiInputWidget(
        items=DEFAULT_REACTION)


class ReactionSchema(Schema):
    """Schema for comment"""

    reaction = colander.SchemaNode(
        colander.String(),
        widget=reaction_widget,
        missing=None,
        )


@view_config(
    name='addreaction',
    context=Emojiable,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AddReactionEmojiableView(FormView):
    schema = select(ReactionSchema(),
                    ['reaction'])
    title = _('Add reaction')
    name = 'addreaction'
    behaviors = [AddReaction]
    viewid = 'addreaction'

    def default_data(self):
        return {'reaction': self.context.get_user_emoji(get_current(self.request))}

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': AddReaction.node_definition.id})
        formwidget = deform.widget.FormWidget(
            css_class='reactionform deform novaideo-ajax-form')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AddReaction: AddReactionEmojiableView})
