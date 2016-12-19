# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import Schema
from pontus.widget import RadioChoiceWidget

from novaideo.content.processes.idea_management.behaviors import (
    MakeOpinion)
from novaideo.content.idea import Idea, OPINIONS
from novaideo.views.widget import LimitedTextAreaWidget
from novaideo import _


@colander.deferred
def opinion_choice(node, kw):
    values = OPINIONS.items()
    return RadioChoiceWidget(values=values)


class OpinionSchema(Schema):
    opinion = colander.SchemaNode(
        colander.String(),
        widget=opinion_choice,
        title=_('Opinion'),
        default='to_study'
        )

    explanation = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=600),
        widget=LimitedTextAreaWidget(rows=5,
                                     cols=30,
                                     limit=600),
        title=_("Explanation")
        )


@view_config(
    name='makeopinionformidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class MakeOpinionFormView(FormView):
    title = _('Give your opinion')
    schema = OpinionSchema()
    behaviors = [MakeOpinion, Cancel]
    formid = 'formmakeopinionidea'
    name = 'makeopinionformidea'

    def default_data(self):
        return getattr(self.context, 'opinion', {})

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': MakeOpinion.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update({MakeOpinion: MakeOpinionFormView})
