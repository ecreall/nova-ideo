# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.view import BasicView
from pontus.form import FormView
from pontus.schema import select, Schema

from novaideo.content.processes.novaideo_abstract_process.behaviors import (
    AddReaction)
from novaideo.core import Emojiable
from novaideo import _
from novaideo.utilities.util import get_emoji_form


@colander.deferred
def reaction_widget(node, kw):
    request = node.bindings['request']
    #TODO get emojis by context
    emoji_form = get_emoji_form(
        request, emoji_class='emoji-input-widget',
        is_grouped=False, add_preview=False,
        items=[':+1:', ':-1:'])
    return deform.widget.TextInputWidget(
        emoji_form=emoji_form,
        template='novaideo:views/templates/emoji_input.pt')


class ReactionSchema(Schema):
    """Schema for comment"""

    reaction = colander.SchemaNode(
        colander.String(),
        widget=reaction_widget
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

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi', query={'op': 'add_reaction'})
        formwidget = deform.widget.FormWidget(css_class='reactionform deform')
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AddReaction: AddReactionEmojiableView})
