# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema

from novaideo.content.processes.novaideo_abstract_process.behaviors import (
    AddDeadLine)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo import _


class DeadlineSchema(Schema):
    """Schema for site configuration."""

    deadline = colander.SchemaNode(
        colander.DateTime(),
        title=_('Deadline')
    )


@view_config(
    name='adddeadline',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AddDeadLineView(FormView):

    title = _('Add the deadline')
    schema = select(DeadlineSchema(), ['deadline'])
    behaviors = [AddDeadLine, Cancel]
    formid = 'formadddeadline'
    name = 'adddeadline'

    @property
    def requirements(self):
        if self.request.locale_name == 'fr':
            return {'css_links': [],
                    'js_links': ['deform:static/pickadate/translations/fr_FR.js']}

        return {'css_links': [],
                 'js_links': []}


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {AddDeadLine: AddDeadLineView})