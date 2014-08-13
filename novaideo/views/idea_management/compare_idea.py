import colander

from zope.interface import invariant
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
    current_version = context.current_version
    values = [(i, i.get_view(request)) for i in current_version.history if not(i is current_version)]
    values = sorted(values, key=lambda v: v[0].modified_at, reverse=True)
    return CheckboxChoiceWidget(values=values, multiple=True)


@colander.deferred
def current_version_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    current_version = context.current_version
    values = [(current_version, current_version.get_view(request))]
    return CheckboxChoiceWidget(values=values, multiple=True)


@colander.deferred
def default_current_version_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = [context.current_version]
    return values


class CompareIdeaSchema(Schema):

    current_version = colander.SchemaNode(
        colander.Set(),
        widget=current_version_choice,
        default=default_current_version_choice,
        missing=[],
        title=_('Current version')
        )

    versions = colander.SchemaNode(
        colander.Set(),
        widget=version_choice,
        title=_('Last versions')
        )
    
    @invariant
    def versions_number_invariant(self, appstruct):
        root = getSite()
        number = 0
        if 'current_version' in appstruct and appstruct['current_version']:
            number += 1

        if 'versions' in appstruct and appstruct['versions']:
            number += len(appstruct['versions'])

        if not(number == 2):
            raise colander.Invalid(self, _('Il selectionner deux versions'))


@view_config(
    name='comparedea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class CompareIdeaView(FormView):

    title = _('Compare idea')
    schema = select(CompareIdeaSchema(), ['current_version', 'versions'])
    behaviors = [CompareIdea]
    formid = 'formcomparedea'
    name='comparedea'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CompareIdea:CompareIdeaView})
