from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.idea_management.behaviors import  Associate
from novaideo.content.correlation import CorrelationSchema, Correlation
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='associate',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class AssociateView(FormView):

    title = _('Associate')
    schema = select(CorrelationSchema(),['comment', 'targets'])
    behaviors = [Associate, Cancel]
    formid = 'formassociate'
    name='associate'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'

DEFAULTMAPPING_ACTIONS_VIEWS.update({Associate:AssociateView})
