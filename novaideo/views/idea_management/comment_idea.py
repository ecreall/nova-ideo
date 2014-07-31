from pyramid.view import view_config

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select

from novaideo.content.processes.idea_management.behaviors import  CommentIdea
from novaideo.content.comment import CommentSchema, Comment
from novaideo.content.idea import Idea
from novaideo import _


@view_config(
    name='commentidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class CommentIdeaView(FormView):

    title = _('Comment')
    schema = select(CommentSchema(factory=Comment, editable=True),['comment', 'attached_files'])
    behaviors = [CommentIdea, Cancel]
    formid = 'formcommentidea'
    name='commentidea'


DEFAULTMAPPING_ACTIONS_VIEWS.update({CommentIdea:CommentIdeaView})
