# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.idea_management.behaviors import (
    CrateAndPublish, CrateAndPublishAsProposal)
from novaideo.content.processes.question_management.behaviors import (
    TransformToIdea)
from novaideo.content.idea import IdeaSchema, Idea
from novaideo.views.proposal_management.create_proposal import add_file_data
from novaideo import _
from novaideo.content.question import Answer


@view_config(
    name='createidea',
    context=Answer,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateIdeaView(FormView):

    title = _('Transform the answer into an idea')
    schema = select(IdeaSchema(factory=Idea, editable=True),
                    ['title',
                     'text',
                     'keywords',
                     'attached_files'])
    behaviors = [CrateAndPublishAsProposal, CrateAndPublish, TransformToIdea, Cancel]
    formid = 'formcreateidea'
    name = 'createidea'

    def default_data(self):
        data = {'text': self.context.comment}
        attached_files = self.context.files
        data['attached_files'] = []
        files = []
        for file_ in attached_files:
            file_data = add_file_data(file_)
            if file_data:
                files.append(file_data)

        if files:
            data['attached_files'] = files

        data['keywords'] = self.context.question.keywords
        return data

    def before_update(self):
        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': TransformToIdea.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {TransformToIdea: CreateIdeaView})
