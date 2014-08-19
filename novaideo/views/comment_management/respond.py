import datetime
from pyramid.view import view_config
from pyramid.threadlocal import get_current_registry

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view_operation import MultipleView
from pontus.view import BasicView, merge_dicts
from pontus.dace_ui_extension.interfaces import IDaceUIAPI

from novaideo.content.processes.comment_management.behaviors import  Respond
from novaideo.content.comment import CommentSchema, Comment
from novaideo import _


@view_config(
    name='respond',
    context=Comment,
    renderer='pontus:templates/view.pt',
    )
class RespondView(FormView):

    title = _('Respond')
    schema = select(CommentSchema(factory=Comment, editable=True),['intention', 'comment'])
    behaviors = [Respond]
    formid = 'formrespond'
    name='respond'


DEFAULTMAPPING_ACTIONS_VIEWS.update({Respond:RespondView})
