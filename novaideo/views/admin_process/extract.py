# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

import colander
from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.widget import Select2Widget

from novaideo.adapters import EXTRACTION_ATTR
from novaideo.content.processes.admin_process.behaviors import (
    Extract)
from novaideo.content.novaideo_application import (
    NovaIdeoApplication)
from novaideo import _
from novaideo.views.filter import FilterView, FilterSchema


@colander.deferred
def attr_choice(node, kw):
    values = [(a, EXTRACTION_ATTR[a]['title']) for a in EXTRACTION_ATTR]
    values = sorted(values, key=lambda a: EXTRACTION_ATTR[a[0]]['order'])
    return Select2Widget(values=values,
                         create=False,
                         multiple=True)


class ExtractionSchema(FilterSchema):

    attributes_to_extract = colander.SchemaNode(
        colander.Set(),
        widget=attr_choice,
        title=_('Attributes to extract'),
        missing=[]
        )


@view_config(
    name='extract',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class ExtractView(FilterView):
    title = _('Extract')
    name = 'extract'
    schema = ExtractionSchema()
    behaviors = [Extract, Cancel]
    formid = 'formextract'
    wrapper_template = 'pontus:templates/views_templates/view_wrapper.pt'
    container_css_class = 'home'

    def before_update(self):
        self.schema = ExtractionSchema()
        super(ExtractView, self).before_update()

DEFAULTMAPPING_ACTIONS_VIEWS.update({Extract: ExtractView})
