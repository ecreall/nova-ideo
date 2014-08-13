import colander

from pyramid.view import view_config
from substanced.util import find_service

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import CheckboxChoiceWidget

from novaideo.content.processes.idea_management.behaviors import  CompareIdea
from novaideo.content.idea import Idea
from novaideo import _


@colander.deferred
def version_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = [(i, i.get_view(request)) for i in context.current_version.history ]
    values = sorted(values, key=lambda v: v[0].modified_at, reverse=True)
    return CheckboxChoiceWidget(values=values, multiple=True)


@colander.deferred
def default_version_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = [context.current_version]
    return values

class CompareIdeaSchema(Schema):

    version = colander.SchemaNode(
        colander.Set(),
        widget=version_choice,
        default=default_version_choice,
        title=_('Version')
        )


@view_config(
    name='comparedea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class CompareIdeaView(FormView):

    title = _('Compare idea')
    schema = select(CompareIdeaSchema(), ['version'])
    behaviors = [CompareIdea]
    formid = 'formcomparedea'
    name='comparedea'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CompareIdea:CompareIdeaView})
