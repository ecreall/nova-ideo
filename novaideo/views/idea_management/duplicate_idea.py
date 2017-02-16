# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
import deform
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, omit

from novaideo.content.processes.idea_management.behaviors import DuplicateIdea
from novaideo.content.idea import Idea, IdeaSchema
from novaideo import _
from ..filter import get_pending_challenges


def add_file_data(file_):
    if file_ and hasattr(file_, 'get_data'):
        return file_.get_data(None)

    return None


@view_config(
    name='duplicateidea',
    context=Idea,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class DuplicateIdeaView(FormView):
    title = _('Duplicate the idea')
    name = 'duplicateidea'
    schema = select(IdeaSchema(), ['challenge',
                                   'title',
                                   'text',
                                   'keywords',
                                   'attached_files',
                                   'note'])
    behaviors = [DuplicateIdea, Cancel]
    formid = 'formduplicateidea'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'

    def before_update(self):
        user = get_current(self.request)
        has_challenges = len(get_pending_challenges(user)) > 0
        if not has_challenges:
            self.schema = omit(
                self.schema, ['challenge'])

        self.action = self.request.resource_url(
            self.context, 'novaideoapi',
            query={'op': 'update_action_view',
                   'node_id': DuplicateIdea.node_definition.id})
        self.schema.widget = deform.widget.FormWidget(
            css_class='deform novaideo-ajax-form')

    def default_data(self):
        data = self.context.get_data(self.schema)
        files = []
        for file_ in data.get('attached_files', []):
            file_data = add_file_data(file_)
            if file_data:
                files.append(file_data)

        if files:
            data['attached_files'] = files

        challenge = self.context.challenge
        if challenge and not challenge.can_add_content:
            data['challenge'] = ''

        return data


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {DuplicateIdea: DuplicateIdeaView})
