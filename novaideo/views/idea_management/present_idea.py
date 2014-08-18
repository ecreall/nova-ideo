import colander
import deform
from pyramid.view import view_config
from substanced.util import find_service

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import Select2WidgetCreateSearchChoice
from pontus.view_operation import MultipleView
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import  PresentIdea
from novaideo.content.idea import Idea
from novaideo import _
from novaideo.mail import PRESENTATION_IDEA_MESSAGE, PRESENTATION_IDEA_SUBJECT


try:
      basestring
except NameError:
      basestring = str


class SetToView(BasicView):
    title = _('Sent to')
    name = 'sentto'
    validators = [PresentIdea.get_validator()]
    template = 'novaideo:views/idea_management/templates/sent_to.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'sentto'


    def update(self):
        members = self.context.persons_contacted
        result = {}
        values = {
                'members': members,
                'basestring': basestring,
               }
        body = self.content(result=values, template=self.template)['body']
        item = self.adapt_item(body, self.viewid)
        result['coordinates'] = {self.coordinates:[item]}
        return result


@colander.deferred
def members_choice(node, kw):
    context = node.bindings['context']
    request = node.bindings['request']
    values = []
    root = getSite(context)
    user = get_current()
    principals = find_service(root, 'principals')
    prop = principals['users'].values()
    values = [(i, i.name) for i in prop if not(user is i)]
    return Select2WidgetCreateSearchChoice(values=values, multiple=True)


class PresentIdeaSchema(Schema):

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        title=_('Recipients')
        )

    subject =  colander.SchemaNode(
        colander.String(),
        default=PRESENTATION_IDEA_SUBJECT,
        title=_('Subject'),
        )

    message = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        default=PRESENTATION_IDEA_MESSAGE,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )

    send_to_me =  colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=_('Send to me'),
        title =_(''),
        missing=False
        )



class PresentIdeaFormView(FormView):

    title = _('Present idea')
    schema = select(PresentIdeaSchema(), ['members', 'subject', 'message', 'send_to_me'])
    behaviors = [PresentIdea]
    formid = 'formpresentideaform'
    name='presentideaform'


@view_config(
    name='presentidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class PresentIdeaView(MultipleView):
    title = _('Present idea')
    name='presentidea'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (PresentIdeaFormView, SetToView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({PresentIdea:PresentIdeaView})
