from pyramid.view import view_config
from substanced.util import get_oid

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import  CreateIdea
from novaideo.content.idea import IdeaSchema, Idea
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _


@view_config(
    name='createidea',
    context=NovaIdeoApplication,
    renderer='pontus:templates/view.pt',
    )
class CreateIdeaView(FormView):

    title = _('Create an idea')
    schema = select(IdeaSchema(factory=Idea, editable=True,
                               omit=['keywords']),
                    ['title',
                     'description',
                     'keywords',
                     'text',
                     'attached_files'])
    behaviors = [CreateIdea, Cancel]
    formid = 'formcreateidea'
    name='createidea'





@view_config(name='createidea',
             context=NovaIdeoApplication,
             xhr=True,
             renderer='json')
class CreateIdeaView_Json(BasicView):

    behaviors = [CreateIdea]

    def creat_idea(self):
        behavior = None
        try:
            behavior = self.behaviorinstances['Create_idea']
            values = {'title': self.params('title'),
                      'description': self.params('description'),
                      'text': ''}
            idea = Idea()
            idea.set_data(values) 
            appstruct= { '_object_data': idea,
                         'keywords': self.params('keywords')}
            behavior.execute(self.context, self.request, appstruct)
            oid = get_oid(idea)
            result = {'oid':str(oid), 'title':idea.title}
            return result
        except Exception:
            return {}


    def __call__(self):
        operation_name = self.params('op')
        if operation_name is not None:
            operation = getattr(self, operation_name, None)
            if operation is not None:
                return operation()

        return {}


DEFAULTMAPPING_ACTIONS_VIEWS.update({CreateIdea: CreateIdeaView})
