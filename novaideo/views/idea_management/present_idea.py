# -*- coding: utf8 -*-
import colander
import deform
from pyramid.view import view_config
from substanced.util import find_service

from dace.processinstance.core import DEFAULTMAPPING_ACTIONS_VIEWS
from dace.util import getSite, find_entities
from dace.objectofcollaboration.principal.util import get_current
from pontus.default_behavior import Cancel
from pontus.form import FormView
from pontus.schema import select, Schema
from pontus.widget import Select2WidgetCreateSearchChoice, Length
from pontus.view_operation import MultipleView
from pontus.view import BasicView

from novaideo.content.processes.idea_management.behaviors import  PresentIdea
from novaideo.content.idea import Idea
from novaideo.content.interface import IPerson
from novaideo import _
from novaideo.mail import PRESENTATION_IDEA_MESSAGE, PRESENTATION_IDEA_SUBJECT


try:
      basestring
except NameError:
      basestring = str



presentidea_message = {'0': _(u"""Pas de personnes contactées"""),
                       '1': _(u"""Une personne contactée"""),
                       '*': _(u"""${len_persons_contacted} personnes contactées""")}


class SentToView(BasicView):
    title = _('Sent to')
    name = 'sentto'
    validators = [PresentIdea.get_validator()]
    template = 'novaideo:views/idea_management/templates/sent_to.pt'
    item_template = 'pontus:templates/subview_sample.pt'
    viewid = 'sentto'


    def update(self):
        members = self.context.persons_contacted
        len_members = len(members)
        index = str(len_members)
        if len_members>1:
            index = '*'

        message = _(presentidea_message[index], mapping={'len_persons_contacted': len_members})
        result = {}
        values = {
                'message': message,
                'members': members,
                'basestring': basestring,
               }
        self.message = message
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
    prop = list(find_entities([IPerson], states=['active']))
    prop.remove(user)
    values = [(i, i.name) for i in prop]
    return Select2WidgetCreateSearchChoice(values=values, multiple=True)


class PresentIdeaSchema(Schema):

    members = colander.SchemaNode(
        colander.Set(),
        widget=members_choice,
        validator = Length(_, min=1, min_message="Vous devez sélectionner au moins {min} membre, ou saisir {min} adresse courrier électronique."),
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

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='controled-form', 
                                              activable=True,
                                              button_css_class="pull-right",
                                              picto_css_class="glyphicon glyphicon-envelope",
                                              button_title="Present")
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='presentidea',
    context=Idea,
    renderer='pontus:templates/view.pt',
    )
class PresentIdeaView(MultipleView):
    title = _('Present the idea')
    description = _('Present the idea')
    name='presentidea'
    template = 'pontus.dace_ui_extension:templates/sample_mergedmultipleview.pt'
    item_template = 'novaideo:views/idea_management/templates/panel_item.pt'
    views = (SentToView, PresentIdeaFormView)

    def get_message(self):
        message = (presentidea_message['0']).format()
        if self.children:
            message = getattr(self.children[0], 'message', message)

        return message

DEFAULTMAPPING_ACTIONS_VIEWS.update({PresentIdea:PresentIdeaView})
