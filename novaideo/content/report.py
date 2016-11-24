# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import colander
from zope.interface import implementer
from pyramid import renderers

from substanced.content import content
from substanced.util import renamer
from substanced.schema import NameSchemaNode

from dace.objectofcollaboration.entity import Entity
from dace.descriptors import (
    SharedUniqueProperty)
from pontus.core import VisualisableElement, VisualisableElementSchema
from pontus.widget import CheckboxChoiceWidget

from .interface import ISReport
from novaideo import _, REPORTING_REASONS
from novaideo.views.widget import LimitedTextAreaWidget

REASON_TEMPLATE = 'novaideo:views/reports_management/templates/reason.pt'


def render_reason(r_id, request, context):
    reason = REPORTING_REASONS.get(r_id)
    return renderers.render(
        REASON_TEMPLATE,
        {'context': context,
         'title': reason['title'],
         'description': reason['description']},
        request)


def context_is_a_report(context, request):
    return request.registry.content.istype(context, 'report')


@colander.deferred
def reporting_reasons_choice(node, kw):
    request = node.bindings['request']
    context = node.bindings['context']
    values = [(r_id, render_reason(r_id, request, context))
              for r_id in REPORTING_REASONS]
    values = sorted(values, key=lambda e: REPORTING_REASONS[e[0]]['order'])
    return CheckboxChoiceWidget(
        values=values,
        multiple=True)


class ReportSchema(VisualisableElementSchema):
    """Schema for working group"""

    name = NameSchemaNode(
        editing=context_is_a_report,
        )

    reporting_reasons = colander.SchemaNode(
        colander.Set(),
        widget=reporting_reasons_choice,
        title=_("Reporting reasons")
        )

    details = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=1200),
        widget=LimitedTextAreaWidget(rows=5,
                                     cols=30,
                                     limit=1200),
        title=_("Details"),
        missing=''
        )


@content(
    'sreport',
    icon='glyphicon glyphicon-align-left',
    )
@implementer(ISReport)
class Report(VisualisableElement, Entity):
    """Working group class"""

    name = renamer()
    templates = {'default': 'novaideo:views/templates/report_result.pt',
                 'bloc': 'novaideo:views/templates/report_result.pt'}
    author = SharedUniqueProperty('author')

    def __init__(self, **kwargs):
        super(Report, self).__init__(**kwargs)
        self.set_data(kwargs)

    def get_reporting_reasons(self):
        return [(REPORTING_REASONS[r]['title'],
                 REPORTING_REASONS[r]['description'])
                for r in self.reporting_reasons]
