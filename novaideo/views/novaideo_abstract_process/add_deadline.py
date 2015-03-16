# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.novaideo_abstract_process.behaviors import  (
    AddDeadLine)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication, NovaIdeoApplicationSchema)
from novaideo import _


@view_config(
    name='adddeadline',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class AddDeadLineView(FormView):

    title = _('Add the deadline')
    schema = select(NovaIdeoApplicationSchema(), ['deadline'])
    behaviors = [AddDeadLine, Cancel]
    formid = 'formadddeadline'
    name = 'adddeadline'

    @property
    def requirements(self):
        if self.request.locale_name == 'fr':
            return {'css_links':[],
                    'js_links':['deform:static/pickadate/translations/fr_FR.js']}

        return {'css_links':[],
                 'js_links':[]}


DEFAULTMAPPING_ACTIONS_VIEWS.update({AddDeadLine: AddDeadLineView})