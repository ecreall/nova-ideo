# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.amendment_management.behaviors import (
    EditAmendment)
from novaideo.content.amendment import AmendmentSchema, Amendment
from novaideo import _


@view_config(
    name='editamendment',
    context=Amendment,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class EditAmendmentView(FormView):
    title = _('Edit the amendment')
    schema = select(AmendmentSchema(factory=Amendment,
                                    editable=True),
                    ['title',
                     'text'])
    behaviors = [EditAmendment, Cancel]
    formid = 'formeditamendment'
    name = 'editamendment'

    def default_data(self):
        return self.context


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {EditAmendment: EditAmendmentView})
