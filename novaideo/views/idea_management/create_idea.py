# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

import pytz
import datetime
from pyramid.view import view_config
from substanced.util import get_oid
from pyramid import renderers

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import get_obj
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import CreateIdea
from novaideo.content.idea import IdeaSchema, Idea
from novaideo.content.novaideo_application import NovaIdeoApplication
from novaideo import _
from novaideo.utilities.util import to_localized_time


@view_config(
    name='createidea',
    context=NovaIdeoApplication,
    renderer='pontus:templates/views_templates/grid.pt',
    )
class CreateIdeaView(FormView):

    title = _('Create an idea')
    schema = select(IdeaSchema(factory=Idea, editable=True),
                    ['title',
                     'text',
                     'keywords',
                     'attached_files'])
    behaviors = [CreateIdea, Cancel]
    formid = 'formcreateidea'
    name = 'createidea'

    def default_data(self):
        localizer = self.request.localizer
        user = get_current()
        time = to_localized_time(
            datetime.datetime.now(tz=pytz.UTC), translate=True)
        title = localizer.translate(_('Idea by'))+' '+\
                getattr(user, 'title', user.name)+' '+\
                localizer.translate(_('the'))+' '+\
                time+' (UTC)'
        return {'title': title}


@view_config(name='ideasmanagement',
             context=NovaIdeoApplication,
             xhr=True,
             renderer='json')
class CreateIdeaView_Json(BasicView):

    idea_template = 'novaideo:views/proposal_management/templates/idea_data.pt'
    behaviors = [CreateIdea]

    def creat_idea(self):
        behavior = None
        try:
            behavior = self.behaviors_instances['Create_an_idea']
            values = {'title': self.params('title'),
                      'text': self.params('text'),
                      'keywords': self.params('keywords')}
            idea = Idea()
            idea.set_data(values)
            appstruct = {'_object_data': idea}
            behavior.execute(self.context, self.request, appstruct)
            oid = get_oid(idea)
            localizer = self.request.localizer
            user = get_current()
            time = to_localized_time(
                datetime.datetime.now(tz=pytz.UTC), translate=True)
            new_title = localizer.translate(_('Idea by'))+' '+\
                    getattr(user, 'title', user.name)+' '+\
                    localizer.translate(_('the'))+' '+\
                    time+' (UTC)'
            data = {'title': idea.title,
                    'oid': str(oid),
                    'body': renderers.render(self.idea_template,
                                             {'idea': idea},
                                             self.request),
                    'new_title': new_title
                    }
            result = data
            return result
        except Exception:
            return {}

    def get_idea(self):
        try:
            oid = int(self.params('oid'))
            idea = get_obj(oid)
            data = {'title': idea.title,
                    'oid': str(oid),
                    'body': renderers.render(self.idea_template,
                                             {'idea': idea},
                                             self.request)
                    }
            result = data
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


DEFAULTMAPPING_ACTIONS_VIEWS.update(
    {CreateIdea: CreateIdeaView})
