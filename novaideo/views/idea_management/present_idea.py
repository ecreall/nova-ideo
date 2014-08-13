import colander

from pyramid.view import view_config
from substanced.util import find_service

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import Select2Widget

from novaideo.content.processes.idea_management.behaviors import  PresentIdea
from novaideo.content.idea import Idea
from novaideo import _


@colander.deferred
def members_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    root = getSite(context)
    principals = find_service(root, 'principals')
    prop = principals['users'].values()
    values = [(i, i.name) for i in prop ]
    return Select2Widget(values=values, multiple=True)


class PresentIdeaSchema(Schema):

    exterior_emails = colander.SchemaNode(
                colander.Sequence(),
                colander.SchemaNode(
                    colander.String(),
                    validator=colander.All(
                        colander.Email(),
                        colander.Length(max=100)
                        ),
                    name=_('Email')
                    ),
                title=_('Exterior emails'),
                description=_("Send the presentation by email")
                )

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Members to invite')
        )


@view_config(
    name='presentidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class PresentIdeaView(FormView):

    title = _('Present idea')
    schema = select(PresentIdeaSchema(), ['members', 'exterior_emails'])
    behaviors = [PresentIdea]
    formid = 'formpresentidea'
    name='presentidea'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'


DEFAULTMAPPING_ACTIONS_VIEWS.update({PresentIdea:PresentIdeaView})
