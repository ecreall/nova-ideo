# -*- coding: utf8 -*-
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

from novaideo.content.processes.amendment_management.behaviors import  PresentAmendment
from novaideo.content.amendment import Amendment
from novaideo import _
from novaideo.mail import PRESENTATION_AMENDMENT_MESSAGE, PRESENTATION_AMENDMENT_SUBJECT
from novaideo.views.idea_management.present_idea import PresentIdeaView, PresentIdeaSchema, SentToView as IdeaSentToView


class SentToView(IdeaSentToView):
    validators = [PresentAmendment.get_validator()]
    template = 'novaideo:views/amendment_management/templates/sent_to.pt'


class PresentAmendmentSchema(PresentIdeaSchema):

    subject =  colander.SchemaNode(
        colander.String(),
        default=PRESENTATION_AMENDMENT_SUBJECT,
        title=_('Subject'),
        )

    message = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=2000),
        default=PRESENTATION_AMENDMENT_MESSAGE,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )


class PresentAmendmentFormView(FormView):

    title = _('Present amendment')
    schema = select(PresentAmendmentSchema(), ['members', 'subject', 'message', 'send_to_me'])
    behaviors = [PresentAmendment]
    formid = 'formpresentamendmentform'
    name='presentamendmentform'

    def before_update(self):
        formwidget = deform.widget.FormWidget(css_class='controled-form', 
                                              activable=True,
                                              button_css_class="pull-right",
                                              picto_css_class="glyphicon glyphicon-envelope",
                                              button_title="Present")
        formwidget.template = 'novaideo:views/templates/ajax_form.pt'
        self.schema.widget = formwidget


@view_config(
    name='presentamendment',
    context=Amendment,
    renderer='pontus:templates/view.pt',
    )
class PresentAmendmentView(PresentIdeaView):
    title = _('Present amendment')
    name='presentamendment'
    views = (SentToView, PresentAmendmentFormView)


DEFAULTMAPPING_ACTIONS_VIEWS.update({PresentAmendment:PresentAmendmentView})
